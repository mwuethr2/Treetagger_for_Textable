"""
<name>Treetagger</name>
<description>creation de Treetagger widget</description>
<icon>path_to_icon.svg</icon>
<priority>11</priority> 
"""
__version__ = u'0.1.0'
# Standard imports...
import Orange
from OWWidget import *
import OWGUI
from _textable.widgets.LTTL.Input import Input
from _textable.widgets.LTTL.Segmenter import Segmenter
from _textable.widgets.LTTL.Segmentation import Segmentation
import subprocess as sp
import os
import re

from _textable.widgets.TextableUtils import *   # Provides several utilities.

class OWTreetagger(OWWidget):
    
    # Widget settings declaration...
    settingsList = [
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
        self.inputs = [('Text Input', Segmentation, self.processInputData), Single]
        self.outputs = [('Text data', Segmentation)]
        
        self.created_inputs = list()
        self.autoSend = True        
        self.options_ttgg = False
        self.langue = 0
        self.word_label = ""
        self.displayAdvancedSettings = False        
        self.label = u'tagged_data'
        self.langues = ["english"]
            
        # Always end Textable widget settings with the following 3 lines...
        self.uuid = None
        self.lien_ttgg = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)

        
        # Settings and other attribute initializations...



            
        # Other attributes...
        self.inputData = None   
        self.segmenter = Segmenter()
        
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------        
        
        # Next two instructions are helpers from TextableUtils. Corresponding
        # interface elements are declared here and actually drawn below (at
        # their position in the UI)...
        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(
            widget=self.controlArea,
            master=self,
            callback=self.sendData,
            infoBoxAttribute=u'infoBox',
            sendIfPreCallback=self.updateGUI,
        )

        # The AdvancedSettings class, also from TextableUtils, facilitates
        # the management of basic vs. advanced interface. An object from this 
        # class (here assigned to self.advancedSettings) contains two lists 
        # (basicWidgets and advanceWidgets), to which the corresponding
        # widgetBoxes must be added.
        self.advancedSettings = AdvancedSettings(
            widget=self.controlArea,
            master=self,
            callback=self.advence,
        )

        # User interface...

        # Advanced settings checkbox (basic/advanced interface will appear 
        # immediately after it...
        self.advancedSettings.draw()

        self.advancedSettings.advancedWidgetsAppendSeparator()
        
        #bouton pour trouver lien ttgg
        self.infoBox3 = OWGUI.widgetBox(
            self.controlArea, 
            u"")
            
        OWGUI.button(
            widget=self.infoBox3,
            master=self,
            label='lien vers treetagger',
            callback = self.browse,
        )
        

        # infoBox1
        self.infoBox1 = OWGUI.widgetBox(
            self.controlArea, 
            u"Language ", 
            addSpace=True)
            
        self.langueBox = OWGUI.comboBox(
            widget = self.infoBox1,
            master = self, 
            value='langue', 
            items = self.langues,
            )
        
        
        # infoBox2 donne des info sur input et output
        self.infoBox2 = OWGUI.widgetBox(self.controlArea, u"Temporaire ")
        
        self.infoLine = OWGUI.widgetLabel( 
            widget = self.infoBox2,              
            label='No input.',
        )    
        
        


        OWGUI.separator(widget=self.controlArea, height=3)

        # From TextableUtils: a minimal Options box (only segmentation label).
        basicOptionsBox = BasicOptionsBox(self.controlArea, self)
 
        OWGUI.separator(widget=self.controlArea, height=3)

        # Now Info box and Send button must be drawn...
        self.infoBox.draw()
        self.sendButton.draw()
        
        # Send data if autoSend.
        #self.sendButton.sendIf()
        
        # aller chercher le lien TreeTagger si pas deja la
        if self.lien_ttgg is None:
            self.browse()
        else:
            self.cacher_bouton(True)
            
        

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
       
#Annotations bloc repris du cours progtextI

    # def annotations(self):

    #     sampled_seg,discarded_seg = segmenter.sample(input_seg, 10)
    #     return sampled_seg.to_string()



    #     filtered_seg, _ = segmenter.select(
    #         input_seg,
    #         re.compile(r'voyelle'),
    #         annotation_key="type",
    #     )
    #     return filtered_seg.to_string()

    #     merged_seg = segmenter.concatenate([sampled_seg, filtered_seg])

    #     return merged.seg.to_string()



    #     for segment in Segmentation:
    #         print segment.annotations ['type']

    #     print [s.annotations['type'] for s in Segementation]
    #     print set ([s.annotations['type']for s in Segementation])

    #     return TextInput.get_annotation_keys()# definitions
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # definitions

    def browse(self):
        self.lien_ttgg = unicode(QFileDialog.getExistingDirectory(self, u'Entrer lien Treetagger'))
        
        print self.lien_ttgg
        if self.lien_ttgg == "" or not self.verifier_treetagger():
            #donne info sur le lien
            self.browse()
        self.saveSettings()


    def verifier_treetagger(self):
        #si reclique sur bouton et change lien desactiver bouton au cas ou lien faux
        self.infoBox2.setDisabled(True)

        # si le lien n'est pas trouvee
        # self.infoLine1.setText("Le lien n'est pas trouve")

        # la liste qu'il devrait avoir
        ttgg_list_folder = ['lib/french-abbreviations', 'cmd/utf8-tokenize.perl', 'bin/tree-tagger.exe' ]
        #attention aux systemes d'explotataion (les fichiers changet (MAC WINDOWS))! import platform

        check = True
        for file_utile in ttgg_list_folder:
            check = check and os.path.isfile( replace(self.lien_ttgg + "/" + file_utile, "//","/") ) # changer (mais verifier le path de treetagger a l'input (doit pas finir avec /))
            if not check:
                break
        return check
            
       
    #recoit l'input
    def processInputData(self, inputData):

        # ici on prend le input 
        self.inputData = inputData
        
        # Send data to output.
        self.sendData()
        
    def sendData(self):
        segmenter = Segmenter()
        # Important: if input data is None, propagate this value to output...
        if not self.inputData:
            #self.infoLine.setText('No input.')
            self.send('Text data', None)
        else:
            #On efface les anciennes valeurs
            self.clearCreatedInputs()
            #self.infoLine.setText(self.inputData.to_string())
            new_segmentations = list()
            for in_segment in self.inputData:
                print("HELLO")
                # On appel la fonction tag
                print in_segment.get_content()
                tagged_text = self.tag(in_segment.get_content())
                # On definit des variables temporaies
                """  [
                ['Hello', 'UH', 'Hello\r'], 
                ['world', 'NN', 'world\r'], 
                ['BOB', 'NP', 'Bob\r'],
                ['bob', 'NN', 'bob\r'], 
                ['bob', 'NN', 'bob\r'], 
                ['']
                ]"""
                
                
                text = "\n".join([elem[0] for elem in tagged_text])
                print text
                new_input = Input(text)
                self.created_inputs.append(new_input) #effacer les input dans delete widget
                new_segmentation = segmenter.tokenize(new_input, [(re.compile(r"\n"), "Split")])

                in_annotations = in_segment.annotations.copy()
                   
                for new_seg_idx in xrange(len(new_segmentation)):
                    new_annotations = in_annotations.copy()
                    new_annotations.update({
                        "POS":  tagged_text[new_seg_idx][1],
                        "lemma": tagged_text[new_seg_idx][2],
                        "word": tagged_text[new_seg_idx][0],   #juste pour verifier                     
                    })
                    new_segmentation[new_seg_idx].annotations = new_annotations
                new_segmentations.append(new_segmentation)
                
                
            output_segmentation = segmenter.concatenate(new_segmentations)
            print(output_segmentation.to_string())

            self.send('Text data', output_segmentation, self)

    def tag(self, inputData) :

        print self.lien_ttgg
        #texte= avec  apres chanque mot et ponctuation \n
        #texte="Bonjour\nca\nva\n?"   #.join(inputData.data) 
        
        ##### ATTENTION POUR LE MOMENT CA NE METS PAS LA PONCTUATION A LA LIGNE ######
       
        ###### !!!!!!!!!!!!!!!!! A FAIRE !!!!!!!!!!!!!!!!!!!!!###################
        
        a_eliminer = ["\n","\t","\r"]
        for ele in a_eliminer:
            inputData = inputData.replace(ele, "")

        replacable = ["?", ",",".","!",":",";","'", " "]
        #TESTER!!!!!!!!!!!!!!!
        for el in replacable:                               #TESTER!!!!!!!!!!!!!!!
            inputData = inputData.replace(el, "\n"+el+"\n")            #TESTER!!!!!!!!!!!!!!!

        inputData = inputData.replace(" \n", "")
        inputData = inputData.replace("\n\n", "\n")
        print(inputData)
        
        tmp = unicode( os.path.expanduser("~/tmp_file.txt") )
        print tmp
        f = open(tmp, 'w')
        f.write(inputData)
        f.close()
        
        print self.langues
        print self.langue

        commande = unicode( self.lien_ttgg + "/" + "bin/tag-" + self.langues[self.langue] + ".bat" )
        print commande
        """ATTENTION: UTILISEZ DIRECTEMENT:
         bin/tree-tagger (MAC LINUX) ou bin/tree-tagger.exe (WINDOWS) 
         pour ajouter des options ajoutez chaque option dans la liste commande:
         exemple: pour la commande contenue dans bin/tag-french.bat:

        commande= [
        "perl", 
        self.lien_ttgg + "cmd\tokenize.pl", 
        "-f", 
        "-a", 
        self.lien_ttgg + "lib\french-abbreviations", 
        tmp, 
        "|", #pas sur peut etre il faut utilise deux appels a sb.Popen (A TESTER)
        self.lien_ttgg + "bin\tree-tagger", 
        self.lien_ttgg + "lib\french.par",
        "-token",
        "-lemma",
        "-sgml",
        "-no-unkown"
        ]
        """

        output = sp.Popen([commande, tmp], stdout=sp.PIPE)
        outtext, err = output.communicate()

        outtmp = outtext.split('\n')
        del(outtext)
        out = []
        for i in xrange(len(outtmp)):
            out.append(outtmp[i].split('\t'))
        return [elem for elem in out if len(elem) == 3]
    
    def cacher_bouton(self,valeur):
        if valeur :
            self.infoBox3.setVisible(False)
            self.infoBox1.setDisabled(False)
        else:
            self.infoBox1.setDisabled(True)
            
            
    def updateGUI(self):
        """Update GUI state"""
        if self.displayAdvancedSettings:
            self.advancedSettings.setVisible(True)
        else:
            self.advancedSettings.setVisible(False)
            
    def advence(self):
        pass
    
    def clearCreatedInputs(self):
        """Delete all Input objects that have been created."""
        # Delete strings...
        for i in self.created_inputs:
            i.clear()
        # Empty list of created inputs.
        del self.created_inputs[:]
        # Delete those created inputs that are at the end of the string store.
        for i in reversed(xrange(len(Segmentation.data))):
            if Segmentation.data[i] is None:
                Segmentation.data.pop(i)
            else:
                break
    
    #fonctionne ?
   
    def onDeleteWidget(self):
        """Free memory when widget is deleted (overriden method)"""
        self.clearCreatedInputs()
        print "Done"
    
    
    def getSettings(self, *args, **kwargs):
        """Read settings, taking into account version number (overriden)"""
        settings = OWWidget.getSettings(self, *args, **kwargs)
        settings["settingsDataVersion"] = __version__.split('.')[:2]
        return settings

    def setSettings(self, settings):
        """Write settings, taking into account version number (overriden)"""
        if settings.get("settingsDataVersion", None) \
                == __version__.split('.')[:2]:
            settings = settings.copy()
            del settings["settingsDataVersion"]
            OWWidget.setSettings(self, settings)
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__=='__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWTreetagger()
    myWidget.show()
    #segmenter = Segmenter()
    myWidget.processInputData(Input("Hello world BOB bob\n bob"))
    myApplication.exec_()
    
