print in_object.to_string()

path = "C:/TreeTagger"

import subprocess as sp
tmp = 'C:/Users/mwuethr2/Desktop/tmp_file.txt'
f = open(tmp, 'w')
f.write("hello\nworld\nin\nthe\nnew\nfile")
f.close()
 
commande = path + "/" + "bin/tag-english.bat"
print commande
out = "C:/Users/mwuethr2/Desktop/out_file.txt"
sp.call([commande, tmp, out ])

f = open(out, 'r')
print f.read()
