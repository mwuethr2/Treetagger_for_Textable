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
import ctypes
#import os

class OWTreetagger(OWWidget):
    
    # Widget settings declaration...
    settingsList = [
        'TextInput',
        'TreetaggerLink',
        'lien_ttgg',
        'options_ttgg'
        'langue'
        'word_label'
        ]   
    
    def __init__(self, parent=None, signalManager=None):
    
        #Widget creator
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0)
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Channel definitions...
        self.inputs = [('TextInput', Segmentation, self.processInputData)]     
        self.outputs = [('Intenger', str)]

        # Settings and other attribute initializations...
        self.TextInput = ""  
        self.TreetaggerLink = Segmenter()
        
        self.options_ttgg = False
        self.langue = "francais"
        self.word_label = ""
        
        self.lien_ttgg = None
        self.loadSettings()
        self.lien_ttgg = None

        # aller chercher le lien TreeTagger si pas deja la
        if self.lien_ttgg is None:
            self.browse()
        
        self.inputData = None   # NB: not a setting.
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------        
        # User interface
        
        OWGUI.checkBox(
            widget=self.controlArea,
            master=self, 
            value="options_ttgg", 
            label="Treetagger options"
            )
            
        OWGUI.comboBox(
            widget=self.controlArea,
            master=self, 
            value='langue', 
            items= ["francais", "anglais"],
            )
            
        # infoBox1
        self.infoBox1 = OWGUI.widgetBox(self.controlArea, u"Option: ", addSpace=True)
        
        OWGUI.lineEdit(
            widget = self.infoBox1,
            master = self,
            value = 'word_label',
            label = 'Output segementation label : ',
            tooltip = "Entrer le label"
        )

        # infoBox3 donne des info sur input et output
        self.infoBox2 = OWGUI.widgetBox(self.controlArea, u"Info : ")
        
        self.infoLine = OWGUI.widgetLabel( 
            widget=self.infoBox2,              
            label='No input.',
        )         
        
        self.infoBox3 = OWGUI.widgetBox(self.controlArea, u"")
        OWGUI.button(
            widget=self.infoBox3, 
            master=self, 
            label='Send', 
            addToLayout=False, 
            default=True,
            #callback = self.verifier_treetagger,
        )
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # definitions
    
    def browse(self):
        self.lien_ttgg = unicode(
            QFileDialog.getExistingDirectory(self, u'Entrer lien Treetagger')
            )
       
        if self.lien_ttgg == "":
            ctypes.windll.user32.MessageBoxA(0, "Entrez un lien, veuillez recommencer !\n\nREMARQUE :\n\nle chemin pour retrouver Treetagger doit contenir 5 fichier:\n- 'bin',\n- 'cmd',\n- 'INSTALL.txt',\n- 'INSTALL.txt~',\n- 'lib',\n- 'README.txt' ", "Erreur", 0) # http://stackoverflow.com/questions/2963263/how-can-i-create-a-simple-message-box-in-python
            self.browse()
            
        else:
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
                
                #remettre compteur a 0 si modifie le lien !
                compteur = 0
                
                # ok le lien est correcte
                return
                
            else:
                #donne info sur le lien
                ctypes.windll.user32.MessageBoxA(0, "Votre lien est incorecte, veuillez recommencer !\n\nREMARQUE :\n\nle chemin pour retrouver Treetagger doit contenir 5 fichier:\n- 'bin',\n- 'cmd',\n- 'INSTALL.txt',\n- 'INSTALL.txt~',\n- 'lib',\n- 'README.txt' ", "Erreur", 0) # http://stackoverflow.com/questions/2963263/how-can-i-create-a-simple-message-box-in-python
                self.browse()
            
            self.saveSettings()
       
    #recoit l'input
    def processInputData(self, inputData):
        """Method that processes the input data (as specified in __init__)."""
        # Store input data in attribute of this widget (so it can be accessed
        # from other methods).
     
        self.inputData = inputData  
        
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
            
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__=='__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWTreetagger()
    myWidget.show()
    #segmenter = Segmenter()
    myWidget.processInputData(u"How are you?")
    myApplication.exec_()
    
