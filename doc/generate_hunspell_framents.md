How to semi-automatically generate fragments for hunspell dictionaries that are most likely correct

# Parse hunspell itself! 

    python code/reparse_composite.py /usr/share/hunspell/de_DE_frami.dic /usr/share/hunspell/de_DE_frami iso8859 1 tmp/hs
    cat tmp/hs tmp/hs_end | sort > hunspell/delta_dic.auto_self

Now use Wikipedia titles

    cat output_de.txt | sort > sorted_de_titles.txt
    python code/reparse_composite.py sorted_de_titles.txt hunspell/de_DE_frami_nhr3 utf8 1 tmp/title
    cat tmp/title tmp/title_end | sort > hunspell/delta_dic_title.auto


Now use some of the most common words in Wikipedia

    cat lists/de/common_25.dic | sort > sorted25
    python code/reparse_composite.py sorted25 /usr/share/hunspell/de_DE_frami utf8 1 tmp/s25
    cat tmp/s25 tmp/s25_end | sort > hunspell/delta_dic_comm25.auto

Now use some less common words from Wikipdia, but require at least 3 occurences

    cat lists/de/common_5.dic | sort | uniq > sorted5
    python code/reparse_composite.py sorted5 /usr/share/hunspell/de_DE_frami utf8 2 tmp/s5
    cat tmp/s5 tmp/s5_end | sort > hunspell/delta_dic_comm5.auto

Now use all words in Wikipdia, but require at least 5 occurences

    cat lists/de/common_all.dic | sort | uniq > sorted_all
    python code/reparse_composite.py sorted_all /usr/share/hunspell/de_DE_frami utf8 4 tmp/hunspell_all4
    cat tmp/hunspell_all4 tmp/hunspell_all4_end  | sort > hunspell/delta_dic_comm_all.auto


Finally, reparse all 

    cat hunspell/delta_dic.auto_self hunspell/delta_dic_comm25.auto \
            hunspell/delta_dic_comm5.auto hunspell/delta_dic_title.auto \
            hunspell/delta_dic_comm_all.auto > /tmp/all.auto
    python code/reparse_composite.py /tmp/all.auto /usr/share/hunspell/de_DE_frami iso8859 0 tmp/reparse
    cat tmp/reparse tmp/reparse_end > hunspell/delta_dic_2nd.auto

Make a copy and add these words to the dictionary

    cp /usr/share/hunspell/de_DE_frami.aff hunspell/de_DE_frami_new.aff
    cp /usr/share/hunspell/de_DE_frami.dic hunspell/de_DE_frami_new.dic

    echo "#" >> hunspell/de_DE_frami_new.dic
    echo "# Automated word fragments (from frami hunspell)" >> hunspell/de_DE_frami_new.dic
    echo "#" >> hunspell/de_DE_frami_new.dic
    echo "" >> hunspell/de_DE_frami_new.dic
    cat hunspell/delta_dic.auto_self >> hunspell/de_DE_frami_new.dic

    echo "" >> hunspell/de_DE_frami_new.dic
    echo "#" >> hunspell/de_DE_frami_new.dic
    echo "# Automated word fragments (from Wikipedia titles)" >> hunspell/de_DE_frami_new.dic
    echo "#" >> hunspell/de_DE_frami_new.dic
    echo "" >> hunspell/de_DE_frami_new.dic
    cat hunspell/delta_dic_title.auto  >> hunspell/de_DE_frami_new.dic

    echo "#" >> hunspell/de_DE_frami_new.dic
    echo "# Automated word fragments (from common 25 Wikipedia words)" >> hunspell/de_DE_frami_new.dic
    echo "#" >> hunspell/de_DE_frami_new.dic
    echo "" >> hunspell/de_DE_frami_new.dic
    cat hunspell/delta_dic_comm25.auto  >> hunspell/de_DE_frami_new.dic

    echo "#" >> hunspell/de_DE_frami_new.dic
    echo "# Automated word fragments (from common 5 Wikipedia words)" >> hunspell/de_DE_frami_new.dic
    echo "#" >> hunspell/de_DE_frami_new.dic
    echo "" >> hunspell/de_DE_frami_new.dic
    cat hunspell/delta_dic_comm5.auto  >> hunspell/de_DE_frami_new.dic

    echo "#" >> hunspell/de_DE_frami_new.dic
    echo "# Automated word fragments (from all Wikipedia words)" >> hunspell/de_DE_frami_new.dic
    echo "#" >> hunspell/de_DE_frami_new.dic
    echo "" >> hunspell/de_DE_frami_new.dic
    cat hunspell/delta_dic_comm_all.auto  >> hunspell/de_DE_frami_new.dic

    echo "#" >> hunspell/de_DE_frami_new.dic
    echo "# Automated word fragments (from second round)" >> hunspell/de_DE_frami_new.dic
    echo "#" >> hunspell/de_DE_frami_new.dic
    echo "" >> hunspell/de_DE_frami_new.dic
    cat hunspell/delta_dic_2nd.auto  >> hunspell/de_DE_frami_new.dic


