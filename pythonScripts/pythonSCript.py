print in_object
tree_tagger = "C:\TreeTagger\bin\tag-french.bat"
#mac
#tree_tagger =  ""
import subprocess as sp
options = ""
sp.popen([tree_tagger, options ])

