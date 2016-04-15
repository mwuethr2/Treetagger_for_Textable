"""
<name>Treetagger</name>
<description>creation de Treetagger widget</description>
<icon>path_to_icon.svg</icon>
<priority>11</priority> 
"""

# Standard imports...
import Orange
from OWWidget import *
import OWGUI
from _textable.widgets.LTTL.Segmenter import Segmenter
from _textable.widgets.LTTL.Segmentation import Segmentation
import PIPEcommunic
import os

class OWTreetagger(OWWidget):
    """Orange widget for adding an integer value to the input"""
    
    # Widget settings declaration...
    settingsList = [
        'InputSegmentation',
        'TreetaggerLink',
        'lien_ttgg',
    ]   
    
    def __init__(self, parent=None, signalManager=None):
        """Widget creator."""
        
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0)

        #----------------------------------------------------------------------
        # Channel definitions...
        self.inputs = [('InputSegmentation', Segmentation, self.processInputData)]     
        self.outputs = [('OutputSegmentation', Segmentation,)]

        #----------------------------------------------------------------------
        # Settings and other attribute initializations...
        self.InputSegmentation = []  
        self.loadSettings()
        self.lien_ttgg = ""
        
        self.inputData = None   # NB: not a setting.
        
        #----------------------------------------------------------------------
        # User interface...
       
        # infoBox1 sert pour trouver le lien vers Treetagger mais manque fonction
        self.infoBox1 = OWGUI.widgetBox(self.controlArea, u"Chemin d'acces vers Treetagger: ", addSpace=True)
        OWGUI.lineEdit(
            widget = self.infoBox1,
            master = self,
            value = 'lien_ttgg',
            label = 'copier le lien ici: ',
            tooltip="Entrer le chemin pour retrouver Treetagger.\nDoit contenir 5 fichier:\n'bin', 'cmd', 'INSTALL.txt', 'INSTALL.txt~', 'lib' et 'README.txt' ",
        )
        OWGUI.button(
            widget=self.infoBox1, 
            master=self, 
            label='Enregistrer', 
            addToLayout=False, 
            default=True,
            callback = self.verifier_treetagger,
        )
        self.infoLine1 = OWGUI.widgetLabel( # NB: using self here enables us to
                                           # access the label in other methods.
            widget=self.infoBox1,              
            label='No input.',
            )
        #----------------------------------------------------------------------

        # infoBox2 noter le nom de l'etiquette
        self.infoBox2 = OWGUI.widgetBox(self.controlArea, u"Option: ")
        OWGUI.lineEdit(
            widget = self.infoBox2,
            master = self,
            value = '',
            label = 'Output segment label: ',
            tooltip="on donne l'identifiant qu'auront chaque segment",
            #callback=self.
        )
        self.infoBox2.setDisabled(True)
        #-----------------------------------------------------------------------

        # infoBox3 donne des info sur input et output
        self.infoBox3 = OWGUI.widgetBox(self.controlArea, u"Option: ")
        
        self.infoLine = OWGUI.widgetLabel( # NB: using self here enables us to
                                           # access the label in other methods.
            widget=self.infoBox3,              
            label='No input.',
        )
        #------------------------------------------------------------------------
         
   
    #----------------------------------------------------------------------------
    # definitions       
    
    
    def verifier_treetagger(self):
        #si reclique sur bouton et change lien desactiver bouton au cas ou lien faux
        self.infoBox2.setDisabled(True)

        # si le lien n'est pas trouvee
        self.infoLine1.setText(
                "Le lien n'est pas trouve"
            )

        # la liste dans son dossier
        ttgg_list_verification = os.listdir('.')

        # la liste qu'il devrait avoir
        ttgg_list_folder = ['bin/tag-french.bat', 'lib/french-abbreviations', 'cmd/utf8-tokenize.perl', 'bin/tree-tagger.exe' ]

        check = True
        for file_utile in ttgg_list_folder:
            check = check and os.path.isfile( replace(self.lien_ttgg + "/" + file_utile, "//","/") ) # changer (mais verifier le path de treetagger à l'input (doit pas finir avec /))
            if not check:
                break

        # je verifier qu'elle soit identique sauf le dernier

        if check:
            self.infoBox2.setDisabled(False)
            #remettre compteur a 0 si modifie le lien !
            compteur = 0
            #donne info sur le lien
            self.infoLine1.setText(
                "Merci, les options sont deverouillees"
            )
        else:
            #donne info sur le lien
            self.infoLine1.setText(
                "Le lien n'est pas correcte"
            )

    
    #recoit l'input
    def processInputData(self, inputData):
        """Method that processes the input data (as specified in __init__)."""
        # Store input data in attribute of this widget (so it can be accessed
        # from other methods).
     
        self.inputData = inputData  
        if self.checkInput():
            self.tagInput()
            """
            # pour desactiver la box si pas de input !
            if inputData is None:
                self.optionsBox.setDisabled(True)
            else:
                self.optionsBox.setDisabled(False)
            """
            # Send data to output.
            self.sendData()
        else:
            #si input pas bon
            pass
    def checkInput(self):
        pass
    
    def tagInput(self):
        treetagger = new PIPEcommunic.TreeTagger(path_to_home=self.lien_ttgg, language='french', 
                 encoding='utf-8', verbose=False, abbreviation_list=None)
        
        mot_ttgg_out = []
        
        for i in xrange(len(self.InputSegmentation.segments)):
            self.ttgg_out = treetagger.tag(self.InputSegmentation.segments[i]) #inputData <- liste de phrases
            original_seg = i
            
            #recreer une segmentation -> qui sera l'output
            self.all_ttgg_out.append(self.ttgg_out)
            
            
        #faire pour tout les input    -->   mot_ttgg = "\n".join(l[0] for l in ttgg_out)
            
           
        
        return self.all_ttgg_out
        
        
    def sendData(self):
        #Compute result of widget processing and send to output
        # Important: if input data is None, propagate this value to output...
        if self.inputData is None:
            self.infoLine.setText('No input.')
            self.send('TreetaggerLink', None)
            
        else:
            result = self.inputData 
            self.infoLine.setText(
                'Il y a %i segment en input ' %len((self.inputData))
            )
            self.send('Treetagger', result)
            

if __name__=='__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWTreetagger()
    myWidget.show()
    #segmenter = Segmenter()
    myWidget.processInputData(u"How are you?")
    myApplication.exec_()
    
