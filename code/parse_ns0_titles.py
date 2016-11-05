
import sys
fname = sys.argv[1]
outname = sys.argv[2]

#fname = "wptitles/dewiki-20151102-all-titles-in-ns0.gz"
import gzip
twords = set([])
with gzip.open(fname, 'rb') as f:
    f.next()
    for l in f:
        title = l.decode("utf8").strip()
        title_words = title.split("_")
        twords.update(title_words)

fixed_words = set([])
thrown = set([])
while twords:
    w = twords.pop()
    if w.isalnum():
        fixed_words.add(w)
    else:
        thrown.add(w)

with open(outname, 'w') as f:
    for w in fixed_words:
        f.write("%s\n" % w.encode("utf8"))

