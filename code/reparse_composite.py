"""
Generate hunspell composite entries by parsing a list of known good words.

This script tries to extract composite words by checking each combination of
suffix and prefix in the list of good words against the current hunspell
database.


"""

import sys


f = open(sys.argv[1], "rb")
hs = sys.argv[2]
FILEENCODING = sys.argv[3]
minocc = int(sys.argv[4]) # 2 used generally
output_fname = sys.argv[5]

import hunspell
# h = hunspell.HunSpell("/usr/share/hunspell/de_DE.dic", "/usr/share/hunspell/de_DE.aff")
# h = hunspell.HunSpell("/usr/share/hunspell/de_DE_frami_nhr.dic", "/usr/share/hunspell/de_DE_frami_nhr.aff")
h = hunspell.HunSpell(hs + ".dic", hs + ".aff")


## FILEENCODING = "utf8"
## FILEENCODING = "iso8859"

word_before = ""
shared_substrings = set([])
gn = 0
stillbad = 0
stillbad_words = []
correct_substrings = dict()
correct_substrings_end = dict()
stillbad_comp_words = []
WORDFRONT = "Abduktoren"
WORDEND = "allergiker"
take_first = True
take_first = False
FUGEN_MINLEN = 6
FUGEN_MINLEN = 5
verbose = True
verbose = False

def checkComposite(baseword, i):
    # check if this word is already entered as composite word (hij)
    is_wordfront = False
    hcheck = baseword[:i].encode("iso8859")  + WORDEND
    if h.spell(hcheck):
        # print "  -> spellched correct", hcheck
        is_wordfront = True

    # check if this word is already entered as composite word (ozm)
    is_wordback = False
    hcheck = WORDFRONT + baseword[i:].encode("iso8859")
    if h.spell(hcheck):
        # print "   -> spellched correct", hcheck
        is_wordback = True

    # print "return" , is_wordfront, is_wordback
    return is_wordfront, is_wordback


for w in f:

    if w.startswith("#") or len(w.strip()) < 2:
        continue

    # convert to unicode string (allows correct access of first character)
    word = w.strip().decode(FILEENCODING)
    baseword = word.split("/")[0]

    if len(baseword.strip()) < 2:
        continue

    ## # Special treatment of previously identified words, we try them again
    ## if word.endswith("/ozm") and word[0].islower():
    ##     baseword = baseword[2].upper() + baseword[1:]

    # We need to be able to encode it for hunspell (skip all words that are not
    # encodeable)
    try:
        hcheck = baseword.encode("iso8859") 
    except UnicodeEncodeError:
        continue

    # Should we skip those which are already correct? 
    # Probably not as they can still yield important information about composite words!
    wordIsCorrect = False
    if h.spell(hcheck):
        gn += 1
        wordIsCorrect = True

    # only use full nouns, discard other words
    if baseword[0].islower():
        continue

    anyCombinationGood = False
    for i in range(4, len(baseword)-3):
        is_wordfront, is_wordback = checkComposite(baseword, i)
        if is_wordfront and is_wordback:
            anyCombinationGood = True
            if verbose:
                print "Is fully composite", baseword[:i].encode("utf8"), " + ", baseword[i:].encode("utf8"), is_wordfront, is_wordback
            break

    if anyCombinationGood:
        continue

    # Start with new word
    if verbose: 
        print "=========================="
        print baseword.encode("utf8")

    # Try every possible suffix/prefix of length 4+ for the good word
    for i in range(4, len(baseword)-3):

        # Create prefix/suffix (capitalized)
        try:
            hcheck = baseword[:i].encode("iso8859") 
            bcheck = baseword[i].upper().encode("iso8859") + baseword[i+1:].encode("iso8859")
        except UnicodeEncodeError:
            # print "Word encoding failed", baseword.encode("utf8")
            continue 

        if verbose:
            print "test", baseword[:i].encode("utf8"), " + ", baseword[i:].encode("utf8")

        # Check if first part of the word is correct (by itself)
        if h.spell(hcheck):

            is_wordfront, is_wordback = checkComposite(baseword, i)

            if verbose: 
                print "correct", hcheck, "back/front:",  is_wordfront, is_wordback, "will check", bcheck

            # Check if second part of the word is correct (by itself)
            if h.spell(bcheck):
                if verbose: print "correct 2nd xx", baseword[:i].encode("utf8"), "+", baseword[i:].encode("utf8")

                # add first word if necessary
                if not is_wordfront:
                    if verbose: print "Will ADD",  baseword[:i ].encode("utf8") 
                    correct_substrings [ baseword[:i] ] = correct_substrings.get( baseword[:i], 0) + 1

                # add second word if necessary
                if not is_wordback:
                    if verbose: print "Will ADD",  baseword[i: ].encode("utf8") 
                    correct_substrings_end [ baseword[i:] ] = correct_substrings_end.get( baseword[i:], 0) + 1

                # Add words that have not yet been deemed to be correct by hunspell
                if not wordIsCorrect:
                    stillbad_comp_words.append( baseword ) 

                # finish composite check
                if take_first:
                    break

            elif baseword[i] == "s" and i > FUGEN_MINLEN and len(baseword) -i > FUGEN_MINLEN:


                bcheck = baseword[i+1].upper().encode("iso8859") + baseword[i+2:].encode("iso8859")

                # This is the case if the first word is correct but not the second one by itself
                # e.g. Zwillingsparadox -> Zwillings/hij
                if baseword[i] == "s":
                    if verbose: print "potential fugen-s, will check", bcheck


                # print "now check", bcheck
                if h.spell(bcheck):
                    if verbose: print "correct 2nd xx with fugen", baseword[:i].encode("utf8"), "+", "s", "+", baseword[i+1:].encode("utf8")

                    is_wordfront = False
                    hcheck = baseword[:i+1].encode("iso8859")  + WORDEND
                    if h.spell(hcheck):
                        is_wordfront = True

                    # add first word if necessary
                    if not is_wordfront:
                        if verbose: print "Will ADD",  baseword[:i+1 ].encode("utf8") 
                        correct_substrings [ baseword[:i+1] ] = correct_substrings.get( baseword[:i+1], 0) + 1

                    # add second word if necessary
                    if not is_wordback:
                        if verbose: print "Will ADD",  baseword[i+1: ].encode("utf8") 
                        correct_substrings_end [ baseword[i+1:] ] = correct_substrings_end.get( baseword[i+1:], 0) + 1

                    # Add words that have not yet been deemed to be correct by hunspell
                    if not wordIsCorrect:
                        stillbad_comp_words.append( baseword ) 

                    # finish composite check
                    if take_first:
                        break


        ## elif h.spell(bcheck):
        ##     print "backword works!! "
        ##     is_wordfront, is_wordback = checkComposite(baseword, i)
        ##     if verbose: print "is wordback ", is_wordback
        ##     if verbose: print "is wordfront ", is_wordfront


        #### else:
        ####     hcheck = baseword[i:].encode("iso8859") 
        ####     if h.spell(hcheck):
        ####         print "correct 2nd only", baseword[:i], "+", baseword[i:]
        ####     ### hcheck = hcheck[0].upper() + hcheck[1:]
        ####     ### # print "test", hcheck
        ####     ### if h.spell(hcheck):
        ####     ###     print "correct 2nd only", baseword[:i], "+", baseword[i:]


    continue
    stillbad += 1
    stillbad_words.append(word)
    longest_shared_substring = ""
    for i in range(5, min(len(word_before), len(word))):
        if word[:i] == word_before[:i]:
            print "Shared substring", word[:i], "in Word", word
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

f  = open(output_fname, "w")
for k, v in correct_substrings.iteritems():
    if verbose:
        print k.encode("utf8"), v
    if v > minocc and len(k) > 4:
        f.write("%s/hij\n" % k.encode("iso8859"))

f  = open(output_fname + "_end", "w")
for k,v in correct_substrings_end.iteritems():
    if verbose:
        print k.encode("utf8"), v
    if v > minocc and len(k) > 4:
        f.write("%s/ozm\n" % k.encode("iso8859"))

f  = open(output_fname + "stillbad", "w")
for s in stillbad_words:
    f.write("%s\n" % s.encode("utf8"))


f  = open(output_fname + "stillbad_c", "w")
for s in set(stillbad_comp_words):
    f.write("%s\n" % s.encode("utf8"))
f.close()

