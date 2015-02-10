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
        while self.text[self.index] == ' ':
            self.next();

        start = self.copy()
        end = start

        if self.new_line():
            self.next()
            return start, end, start.text_to(end)

        while not self.EOF() and self.text[self.index] != ' ' and self.text[self.index] != '\n':
            end = self.copy()
            self.next()

        return start, end, start.text_to(end)

    def EOF(self):
        return self.text[self.index] == EOF_char

    def new_line(self):
        return self.text[self.index] == '\n'

    def next(self):
        if self.index < len(self.text):
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
    tags = {'DECL', 'NTERM', 'TERM', 'NLINE', 'EQUAL'}

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
            self.tokens.append(token)

    def next_token(self):
        NTERM_PATTERN = re.compile("^[A-Z']*$")

        while not self.pos.EOF():
            start, end, word = self.pos.word()

            if word == '\n':
                return Token('NLINE', start, end, "")
            elif word == '=':
                return Token('EQUAL', start, end)
            elif word == '$AXIOM' or word == '$NTERM' or word == '$TERM' or word == '$RULE':
                return Token('DECL', start, end)
            elif word == '$EPS':
                return Token('NTERM', start, end)
            elif word[0] == '\"':
                if (len(word) == 4 and word[1] == '\\' and word[3]=='\"') or \
                   (len(word) == 3 and word[2] == '\"'):
                    return Token('TERM', start, end)
                elif len(word) == 1:
                    _, end, word = self.pos.word()
                    
                    if word == '\"':
                        return Token('TERM', start, end)
                    else:
                        self.errors.append(Token('ERROR', start, end, 'unexpected \"'))
                else:
                    self.errors.append(Token('ERROR', start, end, 'incorrect character'))    
            elif NTERM_PATTERN.match(word):
                return Token('NTERM', start, end)
            else:
                self.errors.append(Token('ERROR', start, end, 'unexpected word'))

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.S = ''
        self.N = []
        self.T = []
        self.P = {} #rulles
        self.errors = []
        self.FIRST = {}
        self.FOLLOW = {}
        self.TABLE = {}

        self.init_syntax_by_tokens()
        for x in self.P:
            for xy in self.P[x]:
                for y in xy:
                    if not self.is_terminal(y) and not y in self.P and y != '$EPS':
                        self.errors.append('ERROR: %s is undeclared NTERM' % y)

        if self.S == '':
            self.errors.append('ERROR: must be at least one axiom')
        self.N += self.S

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
                        while i < len(self.tokens) and self.tokens[i].get_text() != '$RULE':
                            right_elem = []
                            while i < len(self.tokens) and self.tokens[i].tag != 'NLINE':
                                if self.tokens[i].tag == 'NTERM' or self.tokens[i].tag == 'TERM':
                                    right_elem.append(self.tokens[i].get_text())
                                    i+=1
                                else:
                                    self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'unexpected %s, NTERM or TERM expected' % self.tokens[i].tag))
                                    break
                            i+=1
                            right.append(right_elem)
                        self.P[left] = right
                    else:
                        self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, '= expected'))
                        continue
                else:
                    self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'unexpected %s, NTERM expected' % self.tokens[i].tag))
                    continue

            elif self.tokens[i].get_text() == '$AXIOM':
                i+=1
                if self.tokens[i].tag == 'NTERM':
                    if self.S == '':
                        self.S = self.tokens[i].get_text()
                    else:
                        self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'more than one axiom'))
                else:
                    self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'unexpected %s, NTERM expected' % self.tokens[i].tag))
                    continue
                i+=2
            elif self.tokens[i].get_text() == '$NTERM':
                i+=1
                while self.tokens[i].tag != 'NLINE':
                    if self.tokens[i].tag == 'NTERM':
                        text = self.tokens[i].get_text()
                        if text not in self.N:
                            self.N.append(text)
                        else:
                            self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'NTERM %s already exists' % text))    
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
                            self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'TERM %s already exists' % text))    
                    else:
                        self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'unexpected %s, TERM expected' % self.tokens[i].tag))
                        break
                    i+=1
                i+=1
            else:
                i+=1
                self.errors.append(Token('ERROR', self.tokens[i].start, self.tokens[i].end, 'unexpected %s' % self.tokens[i].tag))
                continue

    def init_FIRST(self):
        for nterm in self.N:
            self.FIRST[nterm] = set()

        changed = True
        while changed:
            changed = False
            for nterm in self.N:
                for right in self.P[nterm]:
                    old = copy(self.FIRST[nterm])
                    self.FIRST[nterm] = self.FIRST[nterm].union(self.get_FIRST(right))
                    if old != self.FIRST[nterm]:
                        changed = True

    def is_terminal(self, x):
        return x[0] == '\"'

    def get_FIRST(self, x):
        if len(x) == 0:
            return set(['$EPS'])
        elif x[0] == '$EPS' or self.is_terminal(x[0]):
            return set([x[0]])
        else:
            F= copy(self.FIRST[x[0]])
            if '$EPS' in F:
                F.remove('$EPS')
                F = F.union(self.get_FIRST(x[1:]))
            return F
            

    def init_FOLLOW(self):
        for nterm in self.N:
            self.FOLLOW[nterm] = set()
        self.FOLLOW[self.S].add(EOF_char)

        for X in self.N:
            for uYv in self.P[X]: #X->uYv
                for i in range(len(uYv)-1):
                    Y, v = uYv[i], uYv[i+1:]
                    if not self.is_terminal(Y):
                        S = copy(self.get_FIRST(v)) #FIRST[v]
                        if '$EPS' in S:
                            S.remove('$EPS') #FIRST[v]\eps
                        self.FOLLOW[Y] = self.FOLLOW[Y].union(S)

        changed = True
        while changed:
            changed = False
            for X in self.N:
                for uYv in self.P[X]: #X->uYv
                    for i in range(len(uYv)):
                        Y = uYv[i]
                        if not self.is_terminal(Y) and Y != '$EPS':
                            if i != len(uYv)-1 and uYv[i+1] in self.T:
                                continue
                            old = copy(self.FOLLOW[Y])
                            if i == len(uYv)-1 or '$EPS' in self.FIRST[uYv[i+1]]: #X->uY or eps in FIRST[v]
                                self.FOLLOW[Y] = self.FOLLOW[Y].union(self.FOLLOW[X])
                                if old != self.FOLLOW[Y]:
                                    changed = True

    def init_TABLE(self):
        self.T = self.T + [EOF_char]
        def append_to_table(nterm,term,u):
            if self.TABLE[nterm][term] == ['error']:
                self.TABLE[nterm][term] = set([' '.join(u)])
            else:
                self.TABLE[nterm][term] = self.TABLE[nterm][term].union(u)

        for nterm in self.N:
            self.TABLE[nterm] = {}
            for term in self.T:
                self.TABLE[nterm][term] = ['error']

        for X in self.N: #X->u
            for u in self.P[X]:
                first_u = self.get_FIRST(u)
                for a in first_u:
                    if a != '$EPS':
                        append_to_table(X, a, u)

                if '$EPS' in first_u:
                    for b in self.FOLLOW[X]:
                        append_to_table(X, b, u)
                   

    def print_table(self, filename='table'):
        with open(filename, 'w') as table_file:
            ceil_width = {}
            ceil_width_N = 14
            for t in self.T:
                ceil_width[t] = 0
                for n in self.N:
                    ceil_width[t] = max(len(n), len(', '.join(self.TABLE[n][t])), ceil_width[t])
                ceil_width[t] += 1


            #header
            row = ' '*ceil_width_N + '|'
            for t in self.T:
                row += t.rjust(ceil_width[t])
            table_file.write(row + '\n')

            row = '-'*(sum(ceil_width.values())+1+ceil_width_N)
            table_file.write(row + '\n')

            for n in self.N:
                row = n.rjust(ceil_width_N) + '|'
                for t in self.T:
                    row += ', '.join(self.TABLE[n][t]).rjust(ceil_width[t])
                table_file.write(row + '\n')

    def is_LL1(self):
        for A in self.N:
            r = self.P[A]
            if len(r) > 1:
                for u in r:
                    for v in r:                        
                        if u != v and len(self.get_FIRST(u).intersection(self.get_FIRST(v))) != 0:
                            print "%s -> %s | %s " %(A, u, v)
                            print '\tFIRST[u] =', list(self.get_FIRST(u))
                            print '\tFIRST[v] =', list(self.get_FIRST(v))
                            return False
                        if '$EPS' in self.get_FIRST(v) and len(self.get_FIRST(u).intersection(self.FOLLOW[A])) != 0:
                            print "%s -> %s | %s " %(A, u, v)
                            print '\tFIRST[u] =', list(self.get_FIRST(u))
                            print '\tFOLLOW[A] =', list(self.FOLLOW[A])
                            return False
        return True


class Predictor:
    def __init__(self, text, T, N, S, TABLE):
        self.text = text + EOF_char
        self.T = T + [EOF_char]
        self.N = N
        self.TABLE = TABLE
        self.M = [S, EOF_char] #stack
        self.errors = []
        self.P = {}
        self.i = 0
        self.pos = Position(text)
        self.predict_P()

        for x in self.P:
            new_p_x = []
            for r in self.P[x]:
                Y = r.split(' ')
                while '\"' in Y: #space: " "
                    k = Y.index('\"')
                    Y.pop(k)
                    Y[k] = '\" \"'
                new_p_x.append(Y)
            self.P[x] = new_p_x


    def cover_char(self):
        if self.i >= len(self.text):
            self.i -=1
        char = self.text[self.i]
        if char == '\\':
            self.i+=1
            self.pos.next()
            char += self.text[self.i]
        elif char == '\n':
            char = '\\n'
        elif char == '"':
            char = '\\"'
        elif char == EOF_char:
            return char
        return '"' + char + '"'

    def predict_P(self, print_tree=True):

        tab = 0
        tab_count_S = []
        X = ''
        a = self.cover_char()
        while X != EOF_char: 
            X = self.M[0]
            
            while tab_count_S and tab_count_S[0] == 0:
                tab -=4
                tab_count_S = tab_count_S[1:]
            if tab_count_S:
                tab_count_S[0]-=1
                
            #print 'X=%s, \ta(%d)=%s(%s), \tM=%s' % (X,self.i,a,'self.text[self.i]',self.M)
            if X in self.T:                
                if X == a:
                    self.M = self.M[1:]
                    if print_tree and a != EOF_char:
                        print tab*' ' + X
                    self.i += 1
                    self.pos.next()
                    a = self.cover_char()
                else:
                    self.errors.append('ERROR in non terminal at %d' % self.pos)
                    break
            elif X in self.N:
                if a in self.TABLE[X]:
                    d = list(self.TABLE[X][a])[0]
                else:
                    self.errors.append('ERROR in terminal at %s' % self.pos)
                    break
                if d != 'error':
                    self.M = self.M[1:]
                    Y = d.split(' ')
                    while '\"' in Y: #space: " "
                        k = Y.index('\"')
                        Y.pop(k)
                        Y[k] = '\" \"'

                    self.M = Y + self.M
                    tab_count_S = [len(Y)] + tab_count_S
                    Y = ' '.join(Y)
                    if print_tree:
                        print tab*' ' + X
                        tab += 4

                    if X in self.P:
                        self.P[X].add(Y)
                    else:
                        self.P[X] = set([Y])
                else:
                    self.errors.append('ERROR in terminal at %s' % self.pos)
                    break
            elif X == '$EPS':
                if print_tree:
                    print tab*' ' + X
                self.M = self.M[1:]
                #print 'X=%s, a=%s, M=%s' % (X,a,self.M)

def main():
    import sys
    #gram = open('gram', 'r').read()
    #text = open('gram', 'r').read()
    gram = open('gram1', 'r').read()
    text = open('gram1t', 'r').read()
    lexer = Lexer(gram)
    if lexer.errors:
        for error in lexer.errors:
            print error
        sys.exit(0)
    
    # for token in lexer.tokens:
    #    print token

    parser = Parser(lexer.tokens)
    if parser.errors:
        for error in parser.errors:
            print error
        sys.exit(0)

    # for x in parser.P:
    #     print '%s = %s' % (x, ' | '.join([' '.join(_x) for _x in parser.P[x]]))
    # print '------------------------------'

    parser.init_FIRST()
    # print '------------FIRST-------------'
    # for x in parser.FIRST:
    #     print x, list(parser.FIRST[x])

    parser.init_FOLLOW()
    # print '------------FOLLOW------------'
    # for x in parser.FOLLOW:
    #     print x, list(parser.FOLLOW[x])
    # print '------------------------------'

    if not parser.is_LL1():
        print 'ERROR: not LL1 grammar'
        sys.exit(0)

    parser.init_TABLE()
    parser.print_table()

    predictor = Predictor(text, parser.T, parser.N, parser.S, parser.TABLE)
    if predictor.errors:
        for error in predictor.errors:
            print error
        sys.exit(0)
    # for x in predictor.P:
    #     print '%s = %s' % (x, ' | '.join([' '.join(_x) for _x in predictor.P[x]]))
    #     print '%s = %s' % (x, ' | '.join([' '.join(_x) for _x in parser.P[x]]))

    new_parser = Parser([])
    new_parser.S, new_parser.N, new_parser.T, new_parser.P = parser.S, parser.N, parser.T[:-1], predictor.P
    
    new_parser.init_FIRST()
    # print '------------FIRST-------------'
    # for x in new_parser.FIRST:
    #      print x, list(new_parser.FIRST[x]), list(parser.FIRST[x])

    new_parser.init_FOLLOW()
    # print '------------FOLLOW------------'
    # for x in new_parser.FOLLOW:
    #     print x, list(new_parser.FOLLOW[x])
    # print '------------------------------'

    if not new_parser.is_LL1():
        print 'ERROR: is not LL(1) grammar'
        sys.exit(0)

    new_parser.init_TABLE()
    new_parser.print_table('table1')

    #print 'cmp table table1:'
    #import subprocess
    #subprocess.call('cmp table table1', shell=True)




if __name__ == "__main__":
    main()