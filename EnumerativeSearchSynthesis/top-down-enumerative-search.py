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

    
    
    def is_nonterminal(self, symbol):
        if(symbol in self.prod[symbol]):
           return True
        else:
           return False

    def prod_contains_nonterminal(self, prod):
        for sym in prod:
            if sym in self.prod:
                return True
        return False
    
        

    def gen_sentence(self, Symbol,depth):
        global DEBUG
        global TREE_DEPTH
        if DEBUG:
            print("==== depth = "+str(depth) + "symbol = " + Symbol)
        """ Generate a random sentence from the
            grammar, starting with the given
            symbol.
        """
        # make a list of viable productions according to length
        if(depth <= 0):
#            print("negative depth reached")
#            if depth exhausted only make productions to terminals
            next_prods  = [ p for p in self.prod[Symbol] if not self.prod_contains_nonterminal(p)]
        else:
            next_prods = self.prod[Symbol]
        next_prods.sort(key=len)
        
        los = []
#        print("next_prods = {}".format(next_prods))
        for prod in next_prods:
            if DEBUG:
                print("Prod = {}".format(prod))
            sentence  = ['']
            for sym in prod:
                if DEBUG:
                    print("symbol = {}".format(sym))
            # for non-terminals, recurse
                if sym in self.prod:
                    _sentence = []
                    if sym in self.subs:
                        subs = self.subs[sym]
                    else:
                        depth-=1
                        subs = self.gen_sentence(sym,depth)
                        depth+=1
                    if DEBUG:
                        print("subs = {}".format(subs))
                    for s in sentence:
                        for sub in subs:
                            _sentence.append(s+sub)
                    sentence = _sentence
                        
                else:
                    sentence = [s + sym + ' ' for s in sentence]
                if DEBUG:
                    print("sentence = {}".format(sentence))
            los = los + sentence
            if DEBUG:
                print ("partial sentence = {}".format(sentence))
            if DEBUG:
                print("los = {} sentences added = {}".format(los, sentence))
        if(depth == TREE_DEPTH):
            self.subs[Symbol] = los
        return los

    def get_next_prog(self):
        top = self.q.pop(0)
#        print ("top = {}".format(top))
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
cfg1.add_prod('B', ' ( S < S )|( S = S )|( S > S )|True|False')

if __name__ == '__main__':
    f = open(sys.argv[1])
    reader = csv.reader(f,delimiter=',')
    eg = [(r[0], r[1], r[2]) for r in reader]
    while True:
        p = cfg1.get_next_prog()
        print("Evaluating program {}".format(p))
        correct = 0
        for e in eg:
            print("  Evaluating example {}".format(e))
            p_inst = p.replace('x', e[0])
            p_inst = p_inst.replace('y', e[1])
            print("  Evaluation = %d" % eval(p_inst))
            if (eval(p_inst) == int(e[2])):
                correct+=1;
        if correct == len(eg):
            print(p)
            exit(0)
                
    f.close()
