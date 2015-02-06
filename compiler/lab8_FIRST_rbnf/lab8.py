from copy import copy
import re

EOF_char = chr(1)

class Position:
    def __init__(self, text):
        self.line = 1
        self.pos = 1
        self.index = 0
        self.text = text + EOF_char

    def word(self):
        while not self.EOF() and self.text[self.index] == ' ':
            self.next();

        start = self.copy()
        end = start

        if self.char() == '$':
            while self.text[self.index] != ' ':
                end = self.copy()
                self.next()
        elif self.char() == '"':
            self.next()
            self.next()
            end = self.copy()
            self.next()
        else:
            self.next()
        
        return start, end, start.text_to(end)

    def char(self):
        return self.text[self.index]

    def EOF(self):
        return self.text[self.index] == EOF_char

    def new_line(self):
        return self.text[self.index] == '\n'

    def next(self):
        if not self.text[self.index] == EOF_char:
            self.pos +=1

            if self.new_line():
                self.line += 1
                self.pos = 1
                
            self.index += 1

    def copy(self):
        return copy(self)

    def text_to(self, end):
        return self.text[self.index:end.index+1]

    def __str__(self):
        return '(%s, %s)' % (self.line, self.pos)

class Token:
    tags = {'DECL', 'NTERM', 'TERM', 'NLINE', 'EQUAL', 'OR', 'LBRCKT', 'RBRCKT','LBRACE', 'RBRACE'}

    def __init__(self, tag, start, end, text=None):
        self.start = start
        self.end = end
        self.tag = tag
        self.text = text

    def get_text(self):
        if self.text != None:
            return self.text
        else:
            return self.start.text_to(self.end)

    def __str__(self):
        return '%s \t%s-%s:   \t%s' % (self.tag, self.start, self.end, self.get_text())

class Lexer:
    def __init__(self, text):
        self.tokens = []
        self.errors = []
        self.text = text
        self.pos = Position(text)

        self.analyze()

    def analyze(self):
        while not self.pos.EOF():
            token = self.next_token()
            if token:
                self.tokens.append(token)

    def next_token(self):
        start, end, word = self.pos.word() 

        if word == EOF_char: return None

        if word == '\n':
            return Token('NLINE', start, end)
        elif word == '=':
            return Token('EQUAL', start, end)
        elif word == '(':
            return Token('LBRCKT', start, end)
        elif word == ')':
            return Token('RBRCKT', start, end)
        elif word == '{':
            return Token('LBRACE', start, end)
        elif word == '}':
            return Token('RBRACE', start, end)
        elif word == '|':
            return Token('OR', start, end)
        elif word == '$NTERM' or word == '$TERM' or word == '$RULE':
            return Token('DECL', start, end)
        elif word[0] == '\"':
            if word[2] == '\"':
                return Token('TERM', start, end)
            else:
                self.errors.append(Token('ERROR', start, end, 'unexpected end of TERM'))
        else:
            return Token('NTERM', start, end)

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.S = 'E'
        self.N = []
        self.T = []
        self.P = {} #rulles
        self.errors = []
        self.FIRST = {}

        self.init_syntax_by_tokens()

    def init_syntax_by_tokens(self):
        i = 0
        while i < len(self.tokens):
            if self.tokens[i].get_text() == '$RULE':
                i+=1
                if self.tokens[i].tag == 'NTERM':
                    left = self.tokens[i].get_text()
                    i+=1
                    if self.tokens[i].get_text() == '=':
                        i+=1
                        right = []
                        while i < len(self.tokens) and self.tokens[i].tag != 'NLINE':
                            right.append(self.tokens[i])
                            i+=1
                        self.P[left] = Rule(right)
                        i+=1
                    else:
                        self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, '= expected'))
                        continue
                else:
                    self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'unexpected %s, NTERM expected' % self.tokens[i].tag))
                    continue
            elif self.tokens[i].get_text() == '$NTERM':
                i+=1
                while self.tokens[i].tag != 'NLINE':
                    if self.tokens[i].tag == 'NTERM':
                        text = self.tokens[i].get_text()
                        if text not in self.N:
                            self.N.append(text)
                        else:
                            self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'NTERM %s already declared' % text))    
                    else:
                        self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'unexpected %s, NTERM expected' % self.tokens[i].tag))
                    i+=1
                i+=1
            elif self.tokens[i].get_text() == '$TERM':
                i+=1
                while self.tokens[i].tag != 'NLINE':
                    if self.tokens[i].tag == 'TERM':
                        text = self.tokens[i].get_text()
                        if text not in self.T:
                            self.T.append(text)
                        else:
                            self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'TERM %s already declared' % text))    
                    else:
                        self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'unexpected %s, TERM expected' % self.tokens[i].tag))
                    i+=1
                i+=1
            else:
                i+=1
                self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'unexpected %s' % self.tokens[i].tag))
                continue

    def init_FIRST(self):
        for X in self.P:
            self.FIRST[X] = set()

        changed = True
        while changed:
            changed = False
            for X in self.P:
                u = self.P[X]   #X->u

                old = copy(self.FIRST[X])

                self.FIRST[X] = self.FIRST[X].union(self.get_FIRST(u))

                if old != self.FIRST[X]:
                    changed = True

    def get_FIRST(self, x):
        if x.type == 'TERM':
            return set([x.data])
        elif x.type == 'NTERM':
            return self.FIRST[x.data]
        elif x.type == 'CONCAT':
            [u,v] = x.data
            first_u = self.get_FIRST(u)

            if 'eps' not in first_u:
                return first_u
            else:
                first_u.remove('eps')
                return first_u.union(self.get_FIRST[v])
        elif x.type == 'OR':
            result = set()
            for u in x.data:
                result = result.union(self.get_FIRST(u))
            return result
        elif x.type == 'MANY':
            return self.get_FIRST(x.data).union(set(['eps']))

class Rule:
    def __init__(self, l=[], dont_split=False):
        self.type, self.data = self.parse(l, dont_split)

    def parse(self, l, dont_split):
        if l == []: return None, None        

        if dont_split:
            if l[0].tag == 'NTERM':
                return 'NTERM', l[0].get_text()
            elif l[0].tag == 'TERM':
                return 'TERM', l[0].get_text()
            elif l[0].tag == 'LBRACE':
                return 'MANY', Rule(l[1:-1])
            elif l[0].tag == 'LBRCKT':
                return self.parse(l[1:-1], False)
            else:
                raise Exception('ERROR', 'check syntax at %s' % l[0].start)
        else:
            rules = self.get_rules(l) #[RRR|RRR|RRR]
            or_rules = self.split_rules_by_or(rules) #[[RRR],[RRR],[RRR]]
            or_rules = [self.get_concat(rules) for rules in or_rules] #[R,R,R]
            if len(or_rules) == 1:
                return or_rules[0].type, or_rules[0].data
            else:
                return 'OR', or_rules

    def get_concat(self, rules):
        if len(rules) == 1: return rules[0]

        concat = Rule()
        concat.type = 'CONCAT'
        concat.data = [rules[0], None]

        result = concat

        for rule in rules[1:-1]:
            new_concat = Rule()
            concat.data[1] = new_concat
            new_concat.type = 'CONCAT'
            new_concat.data = [rule, None]
            concat = new_concat

        new_concat = Rule()
        new_concat.type = 'CONCAT'
        concat.data[1] = rules[-1]
        return result

    def split_rules_by_or(self, rules):
        res = []
        elem = []
        for rule in rules:
            if rule != '|':
                elem.append(rule)
            else:
                res.append(elem)
                elem = []
        res.append(elem)
        return res

    def get_rules(self, l):
        rules = []

        rule, l = self.lsplit(l)
        rules.append(rule)

        while l != []:
            rule, l = self.lsplit(l)
            rules.append(rule)

        return rules

    def lsplit(self, l):
        brace_type = None

        if l[0].tag == 'NTERM' or l[0].tag == 'TERM':
            return Rule(l[:1], True), l[1:]
        elif l[0].tag == 'OR':
            return '|', l[1:]
        elif l[0].tag == 'LBRCKT':
            brace_type = 'BRCKT'
        elif l[0].tag == 'LBRACE':
            brace_type = 'BRACE'

        brace_diff = 0
        for i in range(len(l)):
            if l[i].tag == 'L' + brace_type:
                brace_diff += 1
            elif l[i].tag == 'R' + brace_type:
                brace_diff -= 1

            if brace_diff == 0:
                return Rule(l[:i+1], True), l[i+1:]
                after_braces = l[i+1:]
        raise Exception('ERROR', 'L%s at %s without R%s', (brace_type, l[0].start, brace_type))

    def __str__(self):
        return self.type

def print_rule(rule, offset=0):
    print ' '*offset + rule.type

    if rule.type == 'TERM' or rule.type == 'NTERM':
        print ' '*(offset+4), rule.data
    elif rule.type == 'CONCAT' or rule.type =='OR':
        for r in rule.data:
            print_rule(r, offset+4)
    else:
        print_rule(rule.data, offset+4)

def main():
    import sys
    gram = open('gram', 'r').read()

    lexer = Lexer(gram)
    if lexer.errors:
        for error in lexer.errors:
            print error
        sys.exit(0)
    
    # for token in lexer.tokens:
    #     print token

    parser = Parser(lexer.tokens)
    if parser.errors:
        for error in parser.errors:
            print error
        sys.exit(0)

    for x in parser.P:
        print '%s = ' % x
        print_rule(parser.P[x])

    parser.init_FIRST()
    print '------------FIRST-------------'
    for x in parser.FIRST:
        print x, list(parser.FIRST[x])

if __name__ == "__main__":
    main()