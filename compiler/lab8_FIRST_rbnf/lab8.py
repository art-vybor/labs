from copy import copy
import re
import sys

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
    tags = {'NTERM', 'TERM', 'TEXT'}

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

        if word in ['\n', EOF_char]:
            return None
        elif word in ['=', '(', ')', '{', '}', '|', '$NTERM', '$TERM', '$RULE']:
            return Token('TEXT', start, end)
        elif word[0] == '\"':
            if word[2] == '\"':
                return Token('TERM', start, end)
            else:
                self.errors.append(Token('ERROR', start, end, 'unexpected end of TERM'))
        elif word.isalpha() and len(word) == 1:
            return Token('NTERM', start, end)
        else:
            self.errors.append(Token('ERROR', start, end, 'incorrect token'))

class Rule:
    def __init__(self, type, data):
        self.type = type
        self.data = data

    def print_it(self, rule=None, offset=0):
        if rule == None: rule = self
        print ' '*offset + rule.type

        if rule.type == 'TERM' or rule.type == 'NTERM':
            print ' '*(offset+4), rule.data
        elif rule.type == 'CONCAT' or rule.type =='OR':
            for r in rule.data:
                self.print_it(r, offset+4)
        else:
            self.print_it(rule.data, offset+4)

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.S = 'E'
        self.N = []
        self.T = []
        self.P = {} #rulles
        self.FIRST = {}
        self.parseGram()

    # Gram ::= (NtermRow | TermRow | RuleRow)*
    def parseGram(self):
        while not self.EOF():
            if self.token().get_text() == '$NTERM':
                self.parseNtermRow()
            elif self.token().get_text() == '$TERM':
                self.parseTermRow()
            elif self.token().get_text() == '$RULE':
                self.parseRuleRow()
            else:
                self.generate_error('incorrect row at %s, NtermTow, TermRow or RuleRow expected' % self.token().start)

    #NtermRow ::= '$NTERM' Nterm+
    def parseNtermRow(self):
        self.parseString('$NTERM')        
        self.N.append(self.parseNterm())

        while self.token().tag == 'NTERM':
            self.N.append(self.parseNterm())
    
    #TermRow ::= '$TERM' Term+
    def parseTermRow(self):
        self.parseString('$TERM')
        self.T.append(self.parseTerm())

        while self.token().tag == 'TERM':
            self.T.append(self.parseTerm())

    #RuleRow ::= '$RULE' Nterm '=' Rule
    def parseRuleRow(self):
        self.parseString('$RULE')        
        nterm = self.parseNterm()
        self.parseString('=')        
        rule = self.parseRule()

        self.P[nterm] = rule

    #Rule ::= RuleBase ('|' RuleBase)*
    def parseRule(self):
        rules = [self.parseRuleBase()]

        while self.token().get_text() == '|':
            self.parseString('|')
            rules.append(self.parseRuleBase())

        if len(rules) == 1:
            return rules[0]
        else:
            return Rule('OR', rules)

    #RuleBase ::= (Nterm | Term | '{' Rule '}' | '(' Rule ')')+
    def parseRuleBase(self):
        rules = []

        while self.token().tag in ['NTERM', 'TERM'] or self.token().get_text() in '{(':
            if self.token().tag == 'NTERM':
                rules.append(Rule('NTERM', self.parseNterm()))
            elif self.token().tag == 'TERM':
                rules.append(Rule('TERM', self.parseTerm()))
            elif self.token().get_text() == '{':
                self.parseString('{')
                rule = self.parseRule()
                self.parseString('}')
                rules.append(Rule('MANY', rule))
            else: #'('
                self.parseString('(')
                rules.append(self.parseRule())
                self.parseString(')')

        if len(rules) == 0:
            self.generate_error('incorrect rule at %s' % self.token().start)
        elif len(rules) == 1:
            return rules[0]
        else:
            return Rule('CONCAT', rules)

    # Nterm ::= Letter
    def parseNterm(self):
        if self.token().tag == 'NTERM':
            nterm = self.token().get_text()
            self.next()
            return nterm
        self.generate_error('incorrect nterm at %s' % self.token().start)
        
    # Term ::= '"' Nterm '"'
    def parseTerm(self):
        if self.token().tag == 'TERM':
            term = self.token().get_text()
            self.next()
            return term

        self.generate_error('incorrect term at %s' % self.token().start)

    def parseString(self, string):
        if self.token().get_text() != string:
            self.generate_error('incorrect text at %s, %s expected' % (self.token().start, string))
        self.next()

    def EOF(self):
        return self.index == len(self.tokens)

    def token(self):
        if self.EOF():
            return Token('EOF', Position(''), Position(''))
        return self.tokens[self.index]

    def next(self):
        if not self.EOF():
            self.index += 1

    def generate_error(self, text, exit=False):
        raise Exception('ERROR: ', text)

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
            u = x.data[0]
            v = x.data[1:]
            first_u = self.get_FIRST(u)

            if 'eps' not in first_u:
                return first_u
            else:
                first_u.remove('eps')
                if len(v) == 1:
                    return first_u.union(self.get_FIRST(v[0]))
                else:
                    return first_u.union(self.get_FIRST(Rule('CONCAT', v)))
        elif x.type == 'OR':
            result = set()
            for u in x.data:
                result = result.union(self.get_FIRST(u))
            return result
        elif x.type == 'MANY':
            return self.get_FIRST(x.data).union(set(['eps']))

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

    print 'N = ', parser.N
    print 'T = ', parser.T

    for x in parser.P:
        print '%s = ' % x
        parser.P[x].print_it(offset=4)

    parser.init_FIRST()
    print '------------FIRST-------------'
    for x in parser.FIRST:
        print x, list(parser.FIRST[x])

if __name__ == "__main__":
    main()
