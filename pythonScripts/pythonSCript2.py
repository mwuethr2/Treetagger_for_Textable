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

class OWTreetagger(OWWidget):
    """Orange widget for adding an integer value to the input"""
    
    # Widget settings declaration...
    settingsList = [
        'TextInput',
        'TreetaggerLink',
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
        
        self.inputData = None   # NB: not a setting.
        
        #----------------------------------------------------------------------
        # User interface...
       
        # infoBox1 sert pour trouver le lien vers Treetagger mais manque fonction
        self.infoBox1 = OWGUI.widgetBox(self.controlArea, u"Chemin d'acces vers Treetagger: ", addSpace=True)
        OWGUI.lineEdit(
            widget = self.infoBox1,
            master = self,
            value = '',
            label = 'copier le lien ici: ',
            tooltip='on rentre le chemin pour retrouver Treetagger.',
            #callback=self.verifier_treetagger()
        )
        OWGUI.button(
            widget=self.infoBox1, 
            master=self, 
            label='Enregistrer', 
            addToLayout=False, 
            default=True,
            #callback = self.valider(),
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
        #-----------------------------------------------------------------------

        # infoBox3 donne des info sur input et output
        self.infoBox3 = OWGUI.widgetBox(self.controlArea, u"Option: ")
        
        self.infoLine = OWGUI.widgetLabel( # NB: using self here enables us to
                                           # access the label in other methods.
            widget=self.infoBox3,              
            label='No input.',
        )
        #------------------------------------------------------------------------
        
    def verifier_treetagger():
        #qqn doit faire 
        #voir dans si le dossier contient un dossier bin ou lin si oui ok sinon pas ok
        pass
        
    def valider():
        #bla
        pass
    #----------------------------------------------------------------------------
    # def ok :
    
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
    
