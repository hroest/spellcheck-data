Spellcheck Files
================

This repository contains files useful for spellchecking text against a list of known bad words.

## Curated List
The curated list was generated from Benutzer:HRoestTypo/replacedDerivatives

## Common words
The files `lists/de/common_n.dic` contain words that at least `n` times in the German Wikipedia.

## Article tiles
The files `lists/de/titles_de.txt` and  `lists/en/titles_en.txt` contain a list
of words derived from the article tiles of the de and en Wikipedia. These make
a good white list of words that are likely correct (note that there are few
articles in both projects that are redirects of misspelled titles, it might be
smart to exclude those in the future).

You can get the article titles from 

    https://dumps.wikimedia.org/dewiki/latest/

Then you can parse each line by splitting on "\_" and removing stuff like
brackets and then only using unique data.

# Wiktionary


    https://dumps.wikimedia.org/enwiktionary/20161001/
    https://dumps.wikimedia.org/dewiktionary/20161001/

# Dictionary words

An additional set of words was imported from dictionaries freely available online:

    http://ftp.tu-chemnitz.de/pub/Local/urz/ding/de-en/ 
    http://www1.dict.cc/translation_file_request.php  [based on TU Chemnitz wordlist]

    https://www.openthesaurus.de/about/download

# Other projects

Very interesting project that contains many, many words

    https://sourceforge.net/projects/germandict/files/?source=navbar


