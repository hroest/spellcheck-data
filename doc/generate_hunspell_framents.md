How to semi-automatically generate fragments for hunspell dictionaries that are most likely correct

# Parse hunspell itself! 

    python code/reparse_composite.py /usr/share/hunspell/de_DE_frami.dic /usr/share/hunspell/de_DE_frami iso8859 1 tmp/hs
    cat tmp/hs tmp/hs_end > hunspell/delta_dic.auto_self

Now use some of the most common words in Wikipedia

    cat lists/de/common_25.dic | sort > sorted25
    python code/reparse_composite.py sorted25 /usr/share/hunspell/de_DE_frami utf8 1 tmp/s25
    cat tmp/s25 tmp/s25_end > hunspell/delta_dic_comm25.auto

Now use some less common words from Wikipdia, but require at least 3 occurences

    cat lists/de/common_15.dic | sort | uniq > sorted15
    python code/reparse_composite.py sorted15 /usr/share/hunspell/de_DE_frami utf8 2 tmp/s15
    cat tmp/s15 tmp/s15_end > hunspell/delta_dic_comm15.auto

    cat lists/de/common_5.dic | sort | uniq > sorted5
    python code/reparse_composite.py sorted5 /usr/share/hunspell/de_DE_frami utf8 2 tmp/s5
    cat tmp/s5 tmp/s5_end > hunspell/delta_dic_comm5.auto


Now use all words in Wikipdia, but require at least 5 occurences

    cat lists/de/common_all.dic | sort | uniq > sorted_all
    python code/reparse_composite.py sorted_all hunspell/de_DE_frami_nhr3 utf8 4 tmp/hunspell_all4
    cat tmp/hunspell_all4 tmp/hunspell_all4_end  > hunspell/delta_dic_comm_all.auto
