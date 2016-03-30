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
import os

class OWTreetagger(OWWidget):
    """Orange widget for adding an integer value to the input"""
    
    # Widget settings declaration...
    settingsList = [
        'TextInput',
        'TreetaggerLink',
        'lien_ttgg',
    ]   
    
    def __init__(self, parent=None, signalManager=None):
        """Widget creator."""
        
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0)

        #----------------------------------------------------------------------
        # Channel definitions...
        self.inputs = [('TextInput', Segmentation, self.processInputData)]     
        self.outputs = [('Intenger', str)]

        #----------------------------------------------------------------------
        # Settings and other attribute initializations...
        self.TextInput = ""  
        self.TreetaggerLink = Segmenter()
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

        # va dans l'adresse rentre par l'utilisateur
        os.chdir(self.lien_ttgg)

        # la liste dans son dossier
        ttgg_list_verification = os.listdir('.')

        # la liste qu'il devrait avoir
        ttgg_list_folder = ['bin', 'cmd', 'INSTALL.txt', 'INSTALL.txt~', 'lib', 'README.txt']

        # je verifier qu'elle soit identique sauf le dernier
        compteur = 0
        for i in range (len(ttgg_list_folder)):
            if ttgg_list_folder[i] in ttgg_list_verification:
                compteur+=1
        if compteur == len(ttgg_list_folder):
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
        
        """
        # pour desactiver la box si pas de input !
        if inputData is None:
            self.optionsBox.setDisabled(True)
        else:
            self.optionsBox.setDisabled(False)
        """
        
        # Send data to output.
        self.sendData()
        
        
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
    
