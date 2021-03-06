from collections import defaultdict
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

    def number_of_terminals(self, st):
        count = 0
        for sym in st:
            if sym =='x' or sym == 'y':
                count+=1
        return count

    
    def ranking(self, st):
        #penalise if then else
        if('if' in st):
            return len(st)*2
        return len(st)
        
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
            self.q.sort(key=self.ranking)
            top = self.q.pop(0)

        if not self.prod_contains_nonterminal(top):
            #return the top most terminal
            return ' '.join(top)
        
