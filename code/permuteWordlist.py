
def permuteWord(w):
    """Permute the incoming word to find likely misspellings

    Produces 2n -2 permutations:
        n permutations of leaving out one character
        n-2 permutations of switching two characters (the firsts two are not
            switched since this randomly happens as a mistake)
    """

    result = []

    # Leave out one character
    for i in range(len(w)):
        result.append(  w[:i] + w[i+1:] )

    # Switch 2 characters (except the first two)
    for i in range(len(w)-1):
        if i == 0:
            continue

        result.append( w[:i] + w[i+1] + w[i] + w[i+2:] )

    return result


import sys
if len(sys.argv) < 2:
    print "Needs an input file of words as arguments."
    print "Will exit."
    sys.exit()

with open(sys.argv[1]) as f:
    for word in f:
        perm = permuteWord(word.strip())

        for p in perm:
            print "%s;%s" % (p, word.strip())

