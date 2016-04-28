"""
<name>Treetagger</name>
<description>creation de Treetagger widget</description>
<priority>11</priority>
"""

# Standard imports...
import Orange
from OWWidget import *
import OWGUI
from _textable.widgets.LTTL.Segmenter import Segmenter
from _textable.widgets.LTTL.Input import Input
from _textable.widgets.LTTL.Segmentation import Segmentation
import ctypes
import subprocess as sp
import os
import re

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

        self.options_ttgg = False
        self.langue = "francais"
        self.word_label = ""

        self.lien_ttgg = None
        self.loadSettings()

        # aller chercher le lien TreeTagger si pas deja la
        if self.lien_ttgg is None:
            self.browse()

        self.inputData = None   # NB: not a setting.
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------


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
            value = 'word_label', # utiliser self.word_label pour reprendre la valeur entre
            label = 'Output segementation label : ',
            tooltip = "Entrer le label"
        )

        # infoBox3 donne des info sur input et output
        self.infoBox2 = OWGUI.widgetBox(self.controlArea, u"Info : ")

        self.infoLine = OWGUI.widgetLabel(
            widget=self.infoBox2,
            label='Test.',
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

    def browse(self):
        self.lien_ttgg = unicode(QFileDialog.getExistingDirectory(self, u'Entrer lien Treetagger'))
        if self.lien_ttgg == "" or not verifier_treetagger():
            #donne info sur le lien
            self.browse()
        self.saveSettings()


    def verifier_treetagger(self):
        #si reclique sur bouton et change lien desactiver bouton au cas ou lien faux
        self.infoBox2.setDisabled(True)

        # si le lien n'est pas trouvee
        self.infoLine1.setText("Le lien n'est pas trouve")

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
        self.inputs = list()
        segmenter = Segmenter()
        # Important: if input data is None, propagate this value to output...
        if len(self.inputData) == 0:
            self.infoLine.setText('No input.')
            self.send('Text data', None)
        else:
            self.infoLine.setText(self.inputData.to_string())
            for segment in self.inputData:

                # On appel la fonction tag
                tagged_text = self.tag(segment.get_content())

                # On remplis la chaine temporaire (temp_string) des valeurs contenue dans la liste de liste self.inputData_tag
                for element in range(len(tagged_text)-1): #ENLEVER -1 SI PAS DE LIGNES VIDES DANS tag()
                    input = Input(tagged_text[element][0])
                    input.segments[0].annotations.update({
                        'tag': tagged_text[element][1],
                        'lemma': tagged_text[element][2]
                    })
                    self.inputs.append(input)


            seg = segmenter.concatenate(self.inputs)
            print seg.to_string()
            self.infoLine.setText(seg.to_string())
            self.send('Text data', seg, self)


    def tag(self, texte, language='english') :

        #On verifie que l'on a un input et un path pour treetagger:
        if self.lien_ttgg == "" :
            browse()

        replacable = [" ","?", ",",".","!",":",";","'")]    #TESTER!!!!!!!!!!!!!!!
        for el in replacable:                               #TESTER!!!!!!!!!!!!!!!
            texte = texte.replace(el, "\n"+el)              #TESTER!!!!!!!!!!!!!!!

        tmp = 'tmp_file.txt'
        f = open(tmp, 'w')
        f.write(texte)
        f.close()

        commande = [self.lien_ttgg + "/" + "bin/tag-" + language + ".bat", tmp]
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

        output = sp.Popen(commande, stdout=sp.PIPE)
        outtext, err = output.communicate()
        outtmp = outtext.split('\n')
        del(outtext)
        out = []
        for i in xrange(len(outtmp)):
            out.append(outtmp[i].split('\t'))
        return out

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__=='__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWTreetagger()
    myWidget.show()
    input = Input("How are you?")
    myWidget.processInputData(input)
    myApplication.exec_()
