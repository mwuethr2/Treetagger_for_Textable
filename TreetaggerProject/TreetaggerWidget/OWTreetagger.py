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
from _textable.widgets.TextableUtils import * 
from _textable.widgets.LTTL.Input import Input
from _textable.widgets.LTTL.Segmenter import Segmenter
from _textable.widgets.LTTL.Segmentation import Segmentation
import subprocess as sp
import os
import re
import sys

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
        self.autoSend = False
        self.options_ttgg = False
        self.langue = 0
        self.word_label = ""
        self.displayAdvancedSettings = False
        self.label = u'tagged_data'
        self.langues = []


        # Always end Textable widget settings with the following 3 lines...
        self.uuid = None
        self.lien_ttgg = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)


        # Other attributes...
        self.inputData = None
        self.segmenter = Segmenter()

        self.langues_possibles = {
            "francais": ["french.par", "french-abbreviations"],
            "anglais":  ["english-utf8.par", "english-abbreviations"],
            "allemand": ["german-utf8.par", "german-abbreviations"],
            "italien": ["italian-utf8.par","italian-abbreviations"],
            "swahili": ["swahili.par", "swahili-abbreviations"],
            "portuguais" :["portuguese.par", "portuguese-abbreviations"],
            "russe": ["russian.par", "russian-abbreviations"]
        }


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #bouton pour trouver lien ttgg
        self.infoBox3 = OWGUI.widgetBox(
            self.controlArea,
            u"")

        OWGUI.widgetLabel(
            widget = self.infoBox3,
            label=" Rappel :\n\nle chemin pour retrouver Treetagger doit contenir"
                  "5 fichier:\n- 'bin',\n- 'cmd',\n- 'INSTALL.txt',\n- "
                  "'INSTALL.txt~',\n- 'lib',\n- 'README.txt' ",
        )
        OWGUI.button(
            widget=self.infoBox3,
            master=self,
            label='Veuillez entrer le lien correct vers treetagger',
            callback = self.browse,
        )

        # aller chercher le lien TreeTagger si pas deja la
        if self.lien_ttgg is None:
            self.browse()
        else:
            self.initialiser_langue()
            self.afficher_interface(True)


    # definitions

    def browse(self):
        self.lien_ttgg = os.path.normpath(QFileDialog.getExistingDirectory(self, u'Entrer lien Treetagger'), 'utf-8')


        if self.lien_ttgg == "" or not self.verifier_treetagger():
            #donne info sur le lien
            QMessageBox.warning(
                    None,
                    'Textable',
                    "Votre lien est incorrect, veuillez en selectionnez un nouveau !",
                    QMessageBox.Ok
            )

            self.afficher_interface(False)
        else:
            self.initialiser_langue()
            self.afficher_interface(True)
        self.saveSettings()


    def verifier_treetagger(self):

        # la liste qu'il devrait avoir
        ttgg_list_folder = ['cmd/utf8-tokenize.perl', "cmd/tokenize.pl", 'bin/tree-tagger.exe' ]
        #attention aux systemes d'explotataion (les fichiers changet (MAC WINDOWS))! import platform

        check = True
        for file_utile in ttgg_list_folder:
            check = check and os.path.isfile(os.path.normpath(self.lien_ttgg + "/" + file_utile))
            if not check:
                break
        return check


    def initialiser_langue(self):
        # initilise que les langues installees dans treetagger

        # la liste dans son dossier
        langue_verification = os.listdir('.')

        langues_presentes = []
        for langue in self.langues_possibles.keys():
            check = True
            for file_utile in self.langues_possibles[langue]:
                check = check and os.path.isfile( 
                    os.path.normpath(self.lien_ttgg + "/lib/" + file_utile) 
                )
                if not check:
                    break
            if check:
                langues_presentes.append(langue)

        self.langues = langues_presentes
        print ( langues_presentes)
        print (self.langue)
        print (self.langues)

    def afficher_interface(self, valeur):

        self.infoBox3.setVisible(True)

        if valeur :
            self.infoBox3.setVisible(False)

            # User interface...

            self.infoBox = InfoBox(widget=self.controlArea)
            self.sendButton = SendButton(
                widget=self.controlArea,
                master=self,
                callback=self.sendData,
                infoBoxAttribute=u'infoBox',
                sendIfPreCallback=self.updateGUI,
            )

            self.advancedSettings = AdvancedSettings(
                widget=self.controlArea,
                master=self,
                callback=self.advence,
            )


            self.advancedSettings.draw()

            self.advancedSettings.advancedWidgetsAppendSeparator()


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


            OWGUI.separator(widget=self.controlArea, height=3)

            # From TextableUtils: a minimal Options box (only segmentation label).
            basicOptionsBox = BasicOptionsBox(self.controlArea, self)

            OWGUI.separator(widget=self.controlArea, height=3)

            # Now Info box and Send button must be drawn...
            self.infoBox.draw()
            self.sendButton.draw()

            # Send data if autoSend.
            self.sendButton.sendIf()



        # ajuster taille widjet
        self.adjustSize()


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
            self.send('Text data', None)
        else:

            new_segmentations = list()
            for in_segment in self.inputData:

                # Initialize progress bar.
                progressBar = OWGUI.ProgressBar(
                    self,
                    iterations=len(self.inputData)
                )
                tagged_text = self.tag(in_segment.get_content())


                text = "\n".join([elem[0] for elem in tagged_text])
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

                progressBar.advance()   # 1 tick on the progress bar...

            output_segmentation = segmenter.concatenate(new_segmentations)

            self.send('Text data', output_segmentation, self)

            # Clear progress bar.
            progressBar.finish()

    def tag(self, inputData) :
        a_eliminer = ["\n","\t","\r"]
        for ele in a_eliminer:
            inputData = inputData.replace(ele, "")

        replacable = ["?", ",", ".", "!", ":", ";", "'", " "]
        for el in replacable:
            inputData = inputData.replace(el, "\n"+el+"\n")

        inputData = inputData.replace(" \n", "")
        inputData = inputData.replace("\n\n", "\n")
        print(type(inputData))
        tmp = os.path.normpath(os.path.expanduser("~/tmp_file.txt"))
        tmp2 = os.path.normpath(os.path.expanduser("~/tmp_file2.txt"))
        f = open(tmp, 'w')
        f.write(inputData.encode("UTF-8"))
        f.close()

        tmp2 = tmp
        commande2 = [
            os.path.normpath(self.lien_ttgg + "/bin/tree-tagger.exe"),
            os.path.normpath(self.lien_ttgg + "/lib/" + self.langues_possibles[self.langues[self.langue]][0]),
            "-token",
            "-lemma",
            "-sgml",
            "-no-unknown",
            tmp2
        ]
        output = sp.Popen(commande2, stdout=sp.PIPE, shell=False)
        outtext = output.communicate()[0].decode(encoding="utf-8", errors="ignore")
        print(type(outtext))
        outtmp = outtext.split('\n')

        del(outtext)
        out = []
        for i in xrange(len(outtmp)):
            out.append(outtmp[i].split('\t'))
        return [elem for elem in out if len(elem) == 3]


    def updateGUI(self):
        """Update GUI state"""
        if self.displayAdvancedSettings:
            self.advancedSettings.setVisible(True)
        else:
            self.advancedSettings.setVisible(False)


    def advence(self):
        pass
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__=='__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWTreetagger()
    myWidget.show()
    myWidget.processInputData(Input("salut comment vas tu?"))
    myApplication.exec_()

