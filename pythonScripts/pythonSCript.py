print in_object.to_string()

path = "C:/TreeTagger" # chemin treetagger

import subprocess as sp

tmp = 'C:/Users/mwuethr2/Desktop/tmp_file.txt' #creation un fichier temporaire
f = open(tmp, 'w')#ouvre le fichier pour modifier
f.write("hello\nworld\nin\nthe\nnew\nfile") #ecrire un mot ou caractere de ponctuation par ligne
f.close()

commande = path + "/" + "bin/tag-english.bat" #prend le chemin et y ajoute la commande
print commande
out = "C:/Users/mwuethr2/Desktop/out_file.txt" #definie le chemin de l'output du fichier treetagger
sp.call([commande, tmp, out]) # commande = chemin du fichier d'input + chemin du fichier output

f = open(out, 'r')
print f.read()
f.close()
