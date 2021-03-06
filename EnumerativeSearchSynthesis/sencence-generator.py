from collections import defaultdict
import csv
import random
import sys
DEBUG = False
TREE_DEPTH = 3
class CFG(object):
    def __init__(self):
        self.prod = defaultdict(list)
        self.subs = {}
        
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

    def gen_random(self, symbol):
        """ Generate a random sentence from the
            grammar, starting with the given
            symbol.
        """
        sentence = ''
        print('  symbol = {}'.format(symbol))
        # select one production of this symbol randomly
        rand_prod = random.choice(self.prod[symbol])
        print("  prod chosen {}".format(rand_prod))
        for sym in rand_prod:
            # for non-terminals, recurse
            print('  considering sym {} '.format(sym))
            if sym in self.prod:
                sentence += self.gen_random(sym)
            else:
                sentence += sym + ' '
        return sentence

    
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



cfg1 = CFG()
cfg1.add_prod('S', 'x|y|( S + S )|( S if B else S )')
#cfg1.add_prod('S', 'x|y|( S + S )|if( B , S , S )')
cfg1.add_prod('B', ' ( S < S )|( S = S )|( S > S )|True|False')
list_of_expr = cfg1.gen_sentence('S',TREE_DEPTH)
list_of_expr.sort(key=len)
print max(map(len, list_of_expr))
if __name__ == '__main__':
    f = open(sys.argv[1])
    reader = csv.reader(f,delimiter=',')
    eg = [(r[0], r[1], r[2]) for r in reader]
    for p in list_of_expr:
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
