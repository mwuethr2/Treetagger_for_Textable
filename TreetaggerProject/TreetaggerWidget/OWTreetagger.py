"""
<name>Treetagger</name>
<description>creation de Treetagger widget</description>
<icon>TTGG_img.png</icon>
<priority>11</priority>
"""

__version__ = u'0.0.1'

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
import codecs

class OWTreetagger(OWWidget):

    # Widget settings declaration...
    settingsList = [
        'lien_ttgg',
        'lien_lib',
        'lien_bin',
        'lien_cmd',
        'options_ttgg'
        'langue'
        'word_label'
        ]


    def __init__(self, parent=None, signalManager=None):

        #Widget creator
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0)

#---------------------------------------------------------------------------------------------
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
        self.system = os.name


        # Always end Textable widget settings with the following 3 lines...
        self.uuid = None
        self.lien_ttgg = None
        self.lien_lib = None
        self.lien_bin = None
        self.lien_cmd = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)


        # Other attributes...
        self.inputData = None
        self.segmenter = Segmenter()

        self.langues_possibles = {
            "French": ["french.par", "french-abbreviations"],
            "English":  ["english-utf8.par", "english-abbreviations"],
            "German": ["german-utf8.par", "german-abbreviations"],
            "Italian": ["italian-utf8.par", "italian-abbreviations"],
            "Swahili": ["swahili.par", "swahili-abbreviations"],
            "Portuguese" :["portuguese.par", "portuguese-abbreviations"],
            "Russian": ["russian.par", "russian-abbreviations"],
            "Spanish": ["spanish-utf8.par", "spanish-abbreviations", "spanish-mwls"],
            "Slovenian":["slovenian-utf8.par"],
            "Slovak":["slovak2-utf8.par"],
            "Romanian":["romanian.par"],
            "Polish":["polish-utf8.par"],
            "Mongolian":["mongolian.par"],
            "Latin":["latin.par"],
            "Galician":["galician.par"],
            "Finnish":["finnish-utf8.par"],
            "Estonian":["estonian.par"],
            "Bulgarian":["bulgarian-utf8.par"],
            "Spoken French":["spoken-french.par","french-abbreviations"],
            }


#------------------------------------------------------------------------------------------------

        #bouton pour trouver lien ttgg
        self.infoBox3 = OWGUI.widgetBox(
            self.controlArea,
            u"")

        OWGUI.widgetLabel(
            widget=self.infoBox3,
            label="Reminder :\n\nOn Windows\nthe path to find Treetagger must contain"
                  "3 files:\n- 'bin', who must contain 'tree-tagger.exe'"
                  "\n- 'cmd', who must contain 'utf8-tokenize.perl' and 'tokenize.pl'"
                  "\n- 'lib' who contain your setup languages for Treetagger\n\n"
                  "On Mac\nplease enter the three paths to those "
                  "3 files:\n- 'bin', who must contain 'tree-tagger.exe'"
                  "\n- 'cmd', who must contain 'utf8-tokenize.perl' and 'tokenize.pl'"
                  "\n- 'lib' who contain your setup languages for Treetagger",
        )
        if self.system == "nt":
            OWGUI.button(
                widget=self.infoBox3,
                master=self,
                label='Please enter a correct path to treetagger',
                callback=self.browse,
            )
        else:
            self.infoBox_cmd = OWGUI.widgetBox(
                self.controlArea,
                u"")
            OWGUI.button(
                widget=self.infoBox_cmd,
                master=self,
                label='Please enter a correct path to the document cmd',
                callback=self.get_cmd,
            )

            self.infoBox_bin = OWGUI.widgetBox(
                self.controlArea,
                u"")

            OWGUI.button(
                widget=self.infoBox_bin,
                master=self,
                label='Please enter a correct path to the document bin',
                callback=self.get_bin,
            )

            self.infoBox_lib = OWGUI.widgetBox(
                self.controlArea,
                u"")

            OWGUI.button(
                widget=self.infoBox_lib,
                master=self,
                label='Please enter a correct path to the document lib',
                callback=self.get_lib,
            )


        # aller chercher le lien TreeTagger si pas deja la
        if self.system != "nt":
            if self.lien_ttgg is None or self.lien_bin is None or self.lien_cmd is None or self.lien_lib is None:
                self.browse()
            else:
                self.initialiser_langue()
                self.afficher_interface(True)
        else:
            if self.lien_ttgg is None:
                self.browse()
            else:
                self.initialiser_langue()
                self.afficher_interface(True)

    # definitions
    def get_bin(self):
        self.lien_bin = os.path.normpath(unicode(QFileDialog.getExistingDirectory(self, u'Enter a path to bin')))
        if not self.verifier_treetagger():
            self.afficher_interface(False)
        else:
            self.initialiser_langue()
            self.afficher_interface(True)
        self.saveSettings()


    def get_lib(self):
        self.lien_lib = os.path.normpath(unicode(QFileDialog.getExistingDirectory(self, u'Enter a path to lib')))
        if not self.verifier_treetagger():
            self.afficher_interface(False)
        else:
            self.initialiser_langue()
            self.afficher_interface(True)
        self.saveSettings()


    def get_cmd(self):
        self.lien_cmd = os.path.normpath(unicode(QFileDialog.getExistingDirectory(self, u'Enter a path to cmd')))
        if not self.verifier_treetagger():
            self.afficher_interface(False)
        else:
            self.initialiser_langue()
            self.afficher_interface(True)
        self.saveSettings()


    def chemin_acces(self):

        #if self.system == "nt":
        self.lien_lib = os.path.normpath(self.lien_ttgg + "/lib/")
        self.lien_cmd = os.path.normpath(self.lien_ttgg + "/cmd/")
        self.lien_bin = os.path.normpath(self.lien_ttgg + "/bin/")
        #elif self.system in ["o2", "posix"] :
         #   pass
        #else:
         #   pass

    def browse(self):
        self.lien_ttgg = os.path.normpath(unicode(QFileDialog.getExistingDirectory(self, u'Enter a path to Treetagger')))

        self.chemin_acces()

        if self.lien_ttgg == "" or not self.verifier_treetagger():
            #donne info sur le lien
            QMessageBox.warning(
                    None,
                    'Textable',
                    "The path you gave is incorrect, please select a new one!",
                    QMessageBox.Ok
            )

            self.afficher_interface(False)
        else:
            self.initialiser_langue()
            self.afficher_interface(True)
        self.saveSettings()

    def verifier_treetagger(self):

        # la liste qu'il devrait avoir
        if self.system == "nt":
            ttgg_list_folder_cmd = ['utf8-tokenize.perl', "tokenize.pl"]
            folder_bin = 'tree-tagger.exe'
        else:
            ttgg_list_folder_cmd = ['utf8-tokenize.perl', "tokenize.pl"]
            folder_bin = 'tree-tagger'

        check_cmd = True
        check_lib = True
        check_bin = True

        for file_utile1 in ttgg_list_folder_cmd:
            check_cmd = check_cmd and os.path.isfile(os.path.normpath(self.lien_cmd + "/" + file_utile1))
            if not check_cmd:
                break

        check_bin = check_bin and os.path.isfile(os.path.normpath(self.lien_bin + "/" + folder_bin))

        check_lib = check_lib and os.path.isdir(os.path.normpath(self.lien_lib + "/"))

        check = check_bin and check_cmd and check_lib

        if self.system != "nt":
            if check_bin:
                self.infoBox_bin.setVisible(False)
            if check_cmd:
                self.infoBox_cmd.setVisible(False)
            if check_lib:
                self.infoBox_lib.setVisible(False)

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
                    os.path.normpath(self.lien_lib +"/"+ file_utile)
                )
                if not check:
                    break
            if check:
                langues_presentes.append(langue)

        self.langues = langues_presentes


    def afficher_interface(self, valeur):

        self.infoBox3.setVisible(True)

        if valeur:
            if self.system != "nt":
                self.infoBox_lib.setVisible(False)
                self.infoBox_cmd.setVisible(False)
                self.infoBox_bin.setVisible(False)
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
                widget=self.infoBox1,
                master=self,
                value='langue',
                items=self.langues,
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
        self.sendButton.sendIf()

    def sendData(self):
        segmenter = Segmenter()
        # Important: if input data is None, propagate this value to output...
        if not self.inputData:
            self.send('Text data', None)
        else:

            compteur = 0
            for nb_segment in self.inputData:
                taille_segment = self.tag(nb_segment.get_content())
                compteur += len(taille_segment)
            # Initialize progress bar.
            progressBar = OWGUI.ProgressBar(
                self,
                iterations=compteur
            )

            new_segmentations = list()
            for in_segment in self.inputData:

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
                    })
                    new_segmentation[new_seg_idx].annotations = new_annotations
                    progressBar.advance()   # 1 tick on the progress bar...

                new_segmentations.append(new_segmentation)

            output_segmentation = segmenter.concatenate(new_segmentations)
            self.send('Text data', output_segmentation, self)

            # Clear progress bar.
            progressBar.finish()

    def tag(self, inputData):

        tmp = os.path.normpath(os.path.expanduser("~/tmp_file.txt"))
        tmp2 = os.path.normpath(os.path.expanduser("~/tmp_file2.txt"))

        f = open(tmp, 'w')
        f.write(inputData.encode("UTF-8"))
        f.close()
        
        option = ""
        if self.langues[self.langue] == "french":
            option = "-f"
        elif self.langues[self.langue] == "english":
            option = "-e"
        elif self.langues[self.langue] == "italian":
            option = "-i"

        if option:
            commande1 = [
                "perl",
                os.path.normpath(self.lien_cmd + "/" + "utf8-tokenize.perl"),
                option,
                "-a",
                os.path.normpath(self.lien_lib + "/" + self.langues_possibles[self.langues[self.langue]][1]),
                tmp
            ]
        else:
            commande1 = [
                "perl",
                os.path.normpath(self.lien_cmd + "/" + "utf8-tokenize.perl"),
                "-a",
                os.path.normpath(self.lien_lib + "/" + self.langues_possibles[self.langues[self.langue]][1]),
                tmp
            ]

        outcom1 = sp.Popen(commande1, stdout=sp.PIPE)
        out = outcom1.communicate()[0].decode(encoding="utf-8", errors="ignore").replace('\r', '')

        f = codecs.open(tmp2, 'w')
        f.write(out.encode("UTF-8"))
        f.close()


        commande2 = [
            os.path.normpath(self.lien_bin + "/" + "tree-tagger.exe"),
            os.path.normpath(self.lien_lib + "/" + self.langues_possibles[self.langues[self.langue]][0]),
            "-token",
            "-lemma",
            "-sgml",
            "-no-unknown",
            '-quiet',
            tmp2
        ]
        output = sp.Popen(commande2, stdout=sp.PIPE, shell=False)
        outtext = output.communicate()[0].decode(encoding="utf-8", errors="ignore")
        outtmp = outtext.split('\n')

        del outtext
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
 
    def onDeleteWidget(self):
        """Free memory when widget is deleted (overriden method)"""
        self.clearCreatedInputs()

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
#---------------------------------------------------------------------------------

if __name__ == '__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWTreetagger()
    myWidget.show()
    myWidget.processInputData(Input("salut comment vas tu?"))
    myApplication.exec_()
