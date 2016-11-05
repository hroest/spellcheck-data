#!/usr/bin/python
# -*- coding: utf-8  -*-

from pywikibot import xmlreader
from wikispell import textrange_parser
from wikispell import AbstractSpellchecker

import templateparser

aspeller = AbstractSpellchecker.abstract_Spellchecker()

xmlfile = "/media/data/tmp/wiki/dewiktionary-20160111-pages-articles.xml.bz2"
gen = xmlreader.XmlDump(xmlfile).parse()

i = 0
tnames = set([])
tother = set([])
tcollect = set([])
# words = set([])


f_temp = open("dewiktionary_template.txt", "w")
f_links = open("dewiktionary_links.txt", "w")

for i, page in enumerate(gen):
    # print page.ns
    if page.ns == "0":
        text = page.get()
        print i, page.title
        # print text
        templates = templateparser.get_all_templates(text)
        german = True
        for t in templates:
            if t.name == "Sprache":
                # maybe it is another lang?
                german = False
                for v in t.parameters.values():
                    if v == "Deutsch":
                        german = True

        if not german:
            continue

        for t in templates:

            if t.name.find(u"Übersicht") != -1:
                # print "find some uebersicht ", t.name
                if t.name.find(u"Deutsch") != -1:

                    # print t.name, t.parameters
                    for k, v in t.parameters.iteritems():
                        if k in ["Bild", "Genus"]:
                            continue
                        if k.startswith("parameter_"):
                            continue

                        # print k, ":", v
                        # words.update(v)
                        # print v
                        f_temp.write(v.encode("utf8") + "\n")


                    tcollect.update( [t.name] )
                else:
                    tother.update( [t.name] )

            elif len(t.parameters) == 0:
                continue
            elif len(t.parameters) == 1 and len( t.parameters.values()[0] ) == 1:
                # a single construct in a sentence, see https://de.wiktionary.org/wiki/Vorlage:brit.
                continue
                # elif t.name in [ u"iron.", u"ugs.", u"euph.", u"scherzh.", u"übertr.",
                #                "volkst.", "propagand.", "abw.", "landsch.", u"militär.",
                #                 "bildungsspr.", "gaunerspr.", "metaphor." , "antiq.", 
                #                 u'kirchenspr.', u'allg.', u'wiss.', u'urspr.', "handwerksspr.",
                #                ]:
                #     continue
                # elif t.name in [
                #     "Surselv.", u"UEngadin.", u"Sutselv.", u"OEngadin.", u"Surmeir.", # Engadin
                #     "gemgerm.", # old germanic
                #     "nordd.", u"südd.", u"spätmhd.", "westdt.",
                #                 ]:
                #     continue
                # elif t.name in [u'intrans.', u'el', u'trans.', "vatd.", "vorchr.", "kurz", "va.", "geh.", "brit."]:
                #     continue
            elif t.name == "Sprache":
                pass
                # print "Sprache!!", t.parameters.values()
            elif len(t.name) == 2:
                # Language
                continue
            elif t.name in [u"österr.", u"schweiz."]:
                print t.parameters
            elif t.name in ["umg.", "fam.", "geh.", "allg.", "va."]:
                continue
            elif t.name in ["Farsi", "Hebr", "Arab", "Koptisch", "Paschto", ]:
                continue
            elif t.name in [ "Brasilien",
                            "prs", "lld", "syr", "cop", "akk",  u'Urdu', "ckb",
                            ]:
                continue
            elif t.name in ["Lautschrift", "Audio", "audio", u"Hörbeispiele", 
                            "Wortart", "Quellen", "Siehe auch", u"Ü-Tabelle", "Ableitung",
                            "Reim", "Wortbildung", "Internetquelle", u"Vorsätze für Maßeinheiten"]:
                continue
            elif t.name in [u'Kontext', "K", "zeitlich"]:
                # gives context 
                continue
            elif t.name in [u'Alte Schreibweise', "veraltend", "veraltet", "veralteter Wortschatz", "antiq."]:
                # TODO 
                continue
            elif t.name in ["ISSN", u'Wikiquote', u'Wikipedia', "Wikisource", "IPA-Text", "GBS", "Wikispecies", "Commons" ]:
                continue
            elif t.name in [u'erweitern',  u"überarbeiten", u"Übersetzungen umleiten", 
                            u'Beispiele fehlen']:
                continue
            # Other stuff, funny
            elif t.name in [u'Schachbrett']:
                continue
            # Internal stuff
            elif t.name in [ u'QS Herkunft',  u'Wort der Woche', u"Ähnlichkeiten Umschrift", "Grundformverweis", "Lemmaverweis",
                            "QS_Herkunft", "nur Pl.", "Elemente", "Beispiele fehlen", "Grundformverweis Dekl",
                             u'Anmerkung', u'Anmerkungen', "DiB-Projekt Gutenberg-DE", "QS Bedeutungen",
                             u'Per-Focus Online', u'Ähnlichkeiten 2', "Polytonisch", "Anker",
                             u'Ähnlichkeiten 1', u'amer.', u'Per-Zeit Online', u"Löschantrag/Vorlage", "Plainlink", "Herkunft fehlt" ]:
                continue

            elif t.name.startswith("Ref") or \
                t.name.startswith("Per-") or \
                t.name.startswith("Lit"):
                continue
                # print "translation", t.parameters.values()
            elif t.name in [ u"Ü", u"Ü?", u"Üt?", u"Üt", 
                            u"Üxx1", u"Üxx2", u"Üxx3", u"Üxx4", u"Üxx5",
                            u"Üxx1?", u"Üxx2?", u"Üxx3?", u"Üxx4?", u"Üxx5?" ]:
                # print "translation", t.parameters.values()
                continue
            elif len(t.parameters) > 0:
                pass
                # print t.name, t.parameters
                # tnames.update([ t.name ])


        i += 1

        wikilinks = textrange_parser.findRange('[[', ']]', text).ranges
        templates = textrange_parser.findRange('{{', '}}', text).ranges
        templates = aspeller.merge_ranges(templates)
        templates = aspeller.remove_nested_ranges(templates)

        # print wikilinks
        for w in wikilinks:
            word = text[w[0]:w[1]]
            if word.find(":") == -1 and len(word) > 4:
                intemplate = False

                for r in templates:
                    if w[0] > r[0] and w[1] < r[1]:
                        intemplate = True

                if word.startswith("[[#"):
                    continue

                if not intemplate:
                    w2 = word[2:-2].split("|")[0]
                    # words.update(w2)
                    # print w2
                    f_links.write(w2.encode("utf8") + "\n")

    

print "==="
print len(words)
print "==="
print tcollect
print "==="
print tnames
print "==="
print tother


f_temp.close()
f_links.close()

"""

cat dewiktionary_links.txt | sort | uniq  > dewiktionary_links_uniq.txt
cat dewiktionary_template.txt | sort | uniq  > dewiktionary_template_uniq.txt


$ grep -v -i "\." dewiktionary_template_uniq.txt > dewiktionary_template_uniq_.txt
$ grep -v "\-\-" dewiktionary_template_uniq_.txt > dewiktionary_template_uniq__.txt
$ cat split.py 
import fileinput
for line in fileinput.input(): 
        for p in line.split(): 
                    print p

$ cat dewiktionary_template_uniq__.txt | python split.py > dewiktionary_template_uniq___.txt

$ cat dewiktionary_links.txt | python split.py > dewiktionary_links.txt
$ cat dewiktionary_links_uniq.txt | python split.py > dewiktionary_links_uniq_.txt 
$ cat dewiktionary_template_uniq___.txt dewiktionary_links_uniq_.txt | sort | uniq > dewiktionary_words.txt

"""

