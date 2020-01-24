import csv
import random
import sys
from cfg import CFG
cfg1 = CFG()
cfg1.add_prod('S', 'x|y|( S + S )|( S if B else S )')
cfg1.add_prod('B', ' ( S < S )|( S == S )|( S > S )|True|False')

if __name__ == '__main__':
    f = open(sys.argv[1])
    reader = csv.reader(f,delimiter=',')
    eg = [(r[0], r[1], r[2]) for r in reader]
    progs_done=0
    OUTPUT=False
    while True:
        p = cfg1.get_next_prog()
        if(progs_done % 1000) ==0:
            OUTPUT = True
        if(OUTPUT):
            print("{} Programs evaluated".format(progs_done))
            print("Evaluating program {}".format(p))
        correct = 0
        for e in eg:
            if(OUTPUT):
                print("  Evaluating example {}".format(e))
            p_inst = p.replace('x', e[0])
            p_inst = p_inst.replace('y', e[1])
            if(OUTPUT):
                print("  Evaluation = %d" % eval(p_inst))
            if (eval(p_inst) == int(e[2])):
                correct+=1;
        if correct == len(eg):
            print(p)
            exit(0)
        OUTPUT=False
        progs_done+=1
                
    f.close()
