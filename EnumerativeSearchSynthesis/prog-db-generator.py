from collections import defaultdict
import csv
import random
import sys
DEBUG = False
TREE_DEPTH = 2
class CFG(object):
    def __init__(self):
        self.prod = defaultdict(list)
        self.q = ['S']
        self.subs={}
        
    def add_prod(self, lhs, rhs):
        """ Add production to the grammar. 'rhs' can
            be several productions separated by '|'.
            Each production is a sequence of symbols
            separated by whitespace.

            Usage:
                grammar.add_prod('NT', 'VP PP')
                grammar.add_prod('Digit', '1|2|3|4')
        """
        prods = rhs.split('|')
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))

    
    
    def prod_contains_nonterminal(self, prod):
        for sym in prod:
            if sym in self.prod:
                return True
        return False
    
        



    def get_next_prog(self):
        top = self.q.pop(0)
        while self.prod_contains_nonterminal(top):
            i = 0
            while ( top[i] not in self.prod ):
                i+=1
            for p in self.prod[top[i]]:
                n = list(top[:i])
                n +=list(p)
                if (len(top[i+1:]) > 0):
                    n = n + top[i+1:]
                self.q = [n] + self.q
            self.q.sort(key=len)
            top = self.q.pop(0)

        if not self.prod_contains_nonterminal(top):
            #return the top most terminal
            return ' '.join(top)
        
cfg1 = CFG()
cfg1.add_prod('S', 'x|y|( S + S )|( S if B else S )')
cfg1.add_prod('B', ' ( S < S )|( S == S )|( S > S )|True|False')

if __name__ == '__main__':
    f = open(sys.argv[1], 'w')
    i = 0
    while(i<10000000):
        i+=1
        p = cfg1.get_next_prog()
        f.write(p+"\n")
        if i%1000 == 0:
            print("{} exprs written\r".format(i), end='')
    f.close()
