#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Out of 343 674 common words, hunspell alone correctly recognize 244 431 words,
leaving 99 243 words incorrectly flagged as misspelled.

Out of 343 674 common words, hunspell + de-Wikipedia titles correctly recognize
330 811, leaving 12 863 words incorrectly flagged as misspelled.

Out of 343 674 common words, hunspell + de/en-Wikipedia titles correctly
recognize 332 576 words, leaving 11 098 words incorrectly flagged as misspelled.

python ./code/hunspell_falsepos.py ../spellcheck-data/lists/de/common_25.dic  > /tmp/hunspell_ww_25

munch /tmp/hunspell_ww /usr/share/hunspell/de_DE_frami_nhr.aff | sort > /tmp/hunspell_ww_25.dic
hunspell_ww_25.dic

"""

import hunspell
h = hunspell.HunSpell("/usr/share/hunspell/de_DE.dic", "/usr/share/hunspell/de_DE.aff")
# h = hunspell.HunSpell("/usr/share/hunspell/de_DE_frami_nhr.dic", "/usr/share/hunspell/de_DE_frami_nhr.aff")
h2 = hunspell.HunSpell("/usr/share/hunspell/de_CH.dic", "/usr/share/hunspell/de_CH.aff")
h3 = hunspell.HunSpell("/usr/share/hunspell/de_AT.dic", "/usr/share/hunspell/de_AT.aff")

words_total = 0

german_titles = "../spellcheck-data/output_de.txt"
engl_titles = "../spellcheck-data/output_en.txt"

import sys

# A file with known true words, (e.g. occuring more than x times in Wikipedia)
known_true = sys.argv[1]

common_words_dict = set([])
if True:
        f = open(german_titles)
        for i,l in enumerate(f):
            common_words_dict.add(l.strip().decode("utf8").lower())

        f = open(engl_titles)
        for i,l in enumerate(f):
            common_words_dict.add(l.strip().decode("utf8").lower())

h2only = 0
i = 0
for w in open(known_true, "rb"):
    words_total += 1

    if w.find(":") != -1: 
        continue
    if w.decode("utf8").find(u"°") != -1:
        continue

    # print w
    # print w.strip().decode("utf8")
    try:
        ## print w.strip().decode("utf8").encode("iso8859")
        # if not h.spell(w.strip().decode("utf8") ):

        # Check if hunspell sees it as correct (also check Swiss/Austrian forms)
        hcheck = w.strip().decode("utf8").encode("iso8859") 
        if not h.spell( hcheck):
            if not h2.spell(hcheck) and \
                not h3.spell(hcheck):

                    # hunspell believes it is false, check also common Wikipedia titles
                    if w.strip().decode("utf8").lower() not in common_words_dict:
                        i += 1
                        # print i, h.spell(w.strip()), "w '%s' " % w.strip(),  w.strip().decode("utf8").encode("iso8859")
                        print w.strip()
                    else:
                        pass
                        # print "found word only in common_words_dict", w.strip()
            else:
                h2only += 1
    except UnicodeEncodeError:
        pass
        # print "skip", w.strip()

# print "words", words_total
# print "h2 only", h2only


