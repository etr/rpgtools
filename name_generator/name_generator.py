from random import random
from functools import partial
import sys

class ruleObj:
    def __init__(self, svar, srep, dp):
        self.svar = svar
        self.srep = srep
        self.dp = dp

def generateString(sstr, rules = []):
    result = ""
    read = 0
    total = len(sstr)
    do_all = True
    while(read < total):
        buf = ""
        l_idx = sstr.find('<')
        if(l_idx != -1):
            result += sstr[:l_idx]
            read += l_idx + 1
        else:
            result += sstr[:]
            read += len(sstr)
            do_all = False
        result += buf

        if do_all:
            sstr = sstr[l_idx + 1:]
            l_idx = sstr.find('>')
            if(l_idx != -1):
                buf += sstr[:l_idx]
                read += l_idx + 1
                sstr = sstr[l_idx + 1:]
            else:
                result += sstr[:]
                read += len(sstr)
                sstr = ""
        else:
            sstr = ""

        if rules != []:
            r = random()
            for rule in rules:
                if rule.svar == buf:
                    if r < rule.dp:
                        result += rule.srep
                        break
                    r -= rule.dp
    return result

def createRule(ruleList, ruleLine):
    if(ruleLine.strip() != ""):
        parts = ruleLine.split('->')
        rparts = parts[1].rsplit(' ', 1)
        r = ruleObj(parts[0].strip(), rparts[0].strip(), float(rparts[1].strip()))
        ruleList.append(r)

def loadRules(rulesFile):
    fd = open(rulesFile, 'r')
    lines = fd.readlines()
    rules = []
    crule = partial(createRule, rules)
    map(crule, lines)
    return rules

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: python name_generator.py grammar_file"
    else :
        val = "<S>"
        rules = loadRules(sys.argv[1])
        non_terminals = []
        for i in rules:
            for j in rules:
                if( i.srep.find("<" + j.svar + ">") != -1):
                    non_terminals.append(i.svar)
                    break

        terminated = False
        while(not terminated):
            val = generateString(val, rules)
            terminated = True
            for nt in non_terminals:
                if(val.find("<" + nt + ">") != -1):
                    terminated = False
                    break
        val = generateString(val, rules)
        print val
