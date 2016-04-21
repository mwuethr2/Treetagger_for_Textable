path = "C:/TreeTagger"

import subprocess as sp

def tag(texte, language='french',   )

    #texte= avec  après chanque mot et ponctuation \n

    tmp = 'tmp_file.txt'
    f = open(tmp, 'w')
    f.write(texte)
    f.close()
     
    commande = path + "/" + "bin/tag-" + language + ".bat"

    output = sp.Popen([commande, tmp], stdout=sp.PIPE)


    outtext, err = output.communicate()
    outtmp = outtext.split('\n')
    del(outtext)
    out = []
    for i in xrange(outtmp):
        out.append(outtmp[i].split('\t'))
    return out

