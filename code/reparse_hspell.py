

import sys

import hunspell
# h = hunspell.HunSpell("/usr/share/hunspell/de_DE.dic", "/usr/share/hunspell/de_DE.aff")
h = hunspell.HunSpell("/usr/share/hunspell/de_DE_frami_nhr.dic", "/usr/share/hunspell/de_DE_frami_nhr.aff")


f = open(sys.argv[1], "rb")
word_before = ""
shared_substrings = set([])
gn = 0
stillbad = 0
stillbad_words = []
for w in f:
    word = w.strip().decode("utf8")

    baseword = word.split("/")[0]
    hcheck = word.split("/")[0].encode("iso8859") 
    if h.spell(hcheck):
        # print "Word is good now: ", word
        gn += 1
        continue

    print "xx", hcheck

    """
Adjektiv: /A 
Adverb: /C  [ere, eren, erem, ste, sten ... ]

sensitiv/ACozm
"""

    if word.endswith("ung"):
        print "use %s/J" % word[:-3]
    if word.endswith("lich"):
        print "use %s/L" % word[:-4]
    elif word.endswith("ungen"):
        print "use %s/J" % word[:-5]
    elif word.endswith("bar"):
        print "use %s/B" % word[:-3]
    elif word.endswith("isch"):
        print "use %s/A" % word[:-4]
    elif word.endswith("ste"):
        # got adverb
        print "%s/C" % word[:-3]
    elif word[0].islower() and (
        word.endswith("sten") or word.endswith("ster") or word.endswith("stem") or word.endswith("stes")):
        print " special adverb ... ", word
    elif word.endswith("ischen"):
        print "xxx"
    elif word.endswith("bare"):
        print "use %s/B" % word[:-4]
    elif word.endswith("barer") or word.endswith("barem") or word.endswith("bares") or word.endswith("baren"):
        print "use %s/B" % word[:-5]
    elif word.endswith("en"):
        if word[0].isupper():
            print "found plural", word, word[-3]
            smaller = word[:-2]
            if word.endswith("innen"):
                print "use %s/F" % word[:-5]
            elif smaller.endswith("ung"):
                print "use %s/P" % smaller
            elif smaller[-1] in ["t", "g", "l", "f", "p"]:
                print "use %s/N" % word[:-1]
            else:
                # or, ung
                print "use %s/P" % smaller
            if word[-2] in ["n"]:
                pass
        else:
            # Got adjektiv (most likely)
            print "found adj: %s/A" % word[:-2]
    else:
        pass
        #print "dont know"

    continue

    stillbad += 1
    stillbad_words.append(word)
    longest_shared_substring = ""
    for i in range(5, min(len(word_before), len(word))):
        if word[:i] == word_before[:i]:
            # print "Shared substring", word[:i], "in Word", word
            longest_shared_substring = word[:i]

    if longest_shared_substring != "":
        print "Shared substring", longest_shared_substring, "in Word", word, "( and other word %s)" % word_before
        if longest_shared_substring[0].isupper():
            shared_substrings.add(longest_shared_substring)

    word_before = word


print "nr shared subs", len(shared_substrings)
print "good now", gn
print "still bad ", stillbad
# good now 2282
# still bad  7404


# sys.exit()

f  = open("output", "w")
for s in shared_substrings:
    f.write("%s/hij\n" % s.encode("iso8859"))

f  = open("stillbad", "w")
for s in stillbad_words:
    f.write("%s\n" % s.encode("utf8"))

f.close()

