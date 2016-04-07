path = "C:/TreeTagger"

import subprocess as sp
tmp = 'C:/Users/mwuethr2/Desktop/tmp_file.txt'
f = open(tmp, 'w')
f.write("hello\nworld\nin\nthe\nnew\nfile")
f.close()
 
commande = path + "/" + "bin/tag-english.bat"

output = sp.Popen([commande, tmp], stdout=sp.PIPE)


out, err = output.communicate()

print out

print err
