from copy import deepcopy

def symbol_type(symbol):
    for i in range(len(symbol_types)):
        if symbol in symbol_types[i]:
            return i
    return -1

def str_pos(position):
    return '(%s, %s)' % (position['line'], position['column'])

def inc_pos(position):
    if text[i] == '\n': 
        return {'line': position['line'] + 1, 'column': 1}

    return {'line': position['line'], 'column': position['column'] + 1}



final_states = set(['space', 'number', 'keyword', 'ident'])

symbol_types = [
    ' \t\n', #space
    '0123456789', #digit
    'i', #keyword letters
    'n',
    't',
    'f',
    'l',
    'o',
    'a',
    'ABCDEFGHIJKLMOPQRSTUVWXYZbcdeghjkmpqrsuvwxyz',   #letters without keyword letters
]

final_state_machine = [
#    space,    digit, i,        n,        t,         f,        l,        o,        a,        letter 
    ['space',  1,     2,        7,        7,         4,        7,        7,        7,        7       ],  #0
    ['number', 1,     'number', 'number', 'number',  'number', 'number', 'number', 'number', 'number'],  #1
    ['ident',  7,     7,        3,        7,         7,        7,        7,        7,        7       ],  #2
    ['ident',  7,     7,        7,        'keyword', 7,        7,        7,        7,        7       ],  #3
    ['ident',  7,     7,        7,        7,         7,        5,        7,        7,        7       ],  #4
    ['ident',  7,     7,        7,        7,         7,        7,        6,        7,        7       ],  #5
    ['ident',  7,     7,        7,        7,         7,        7,        7,        3,        7       ],  #6
    ['ident',  7,     7,        7,        7,         7,        7,        7,        7,        7       ],  #7
]    

EOF = chr(0x01)
text = open('source', 'r').read() + ' ' + EOF

position = {'line': 1, 'column': 1}
start_position, state, i, start_i = position, 0, 0, 0
updateStart = False

while text[i] != EOF:
    
    s_type = symbol_type(text[i])
    #print '%c in %s' % (text[i], symbol_types[s_type])

    if s_type == -1:
        print 'error %s: incorrect symbol %c' % (str_pos(position), text[i])
        updateStart = True
    else:
        #print "'%c': %s, state=%s" % (text[i], str_pos(position), state)
        state = final_state_machine[state][s_type]

        if state in final_states:
            if state == 'keyword':
                print '%s %s-%s: %s' % (state, str_pos(start_position), str_pos(position), text[start_i:i+1])
                updateStart = True
            elif state in {'ident', 'number'}:
                print '%s %s-%s: %s' % (state, str_pos(start_position), str_pos(prev_position), text[start_i:i])
                start_position, start_i, state = position, i, 0
                continue
            elif state == 'space':
                updateStart = True
                
    prev_position, position, i = position, inc_pos(position), i + 1

    if updateStart:
        start_position, start_i, state = position, i, 0
        updateStart = False 
    