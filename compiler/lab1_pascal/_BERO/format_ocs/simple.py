import codecs

def split(line):
    i = 0
    
    while i < len(line):
        if line[i] == '#':
            #print '#: %d' % i
            block='#'
            i+=1
            while i < len(line) and line[i].isdigit():
                block+=line[i]
                i+=1
            yield block

        elif line[i] == '\'':
            #print '\': %d' % i
            i+=1
            while i < len(line):
                if line[i] == '\'':
                    if i+1 < len(line) and line[i+1] == '\'':
                        yield '\'\'\'\''
                        i+=2
                        continue
                    else:
                        i+=1
                        break

                yield '\'' + line[i] + '\''
                i+=1

with codecs.open('in', mode='r', encoding='utf-8') as input_file:
    ocs_in = []
    for line in input_file:
        line = line.rstrip('\r\n')
        ocs_in.extend(split(line))

    with codecs.open('out', 'w', encoding='utf-8') as output_file:
        for elem in ocs_in:
            output_file.write(' OCC(%s);\n' % (elem))






        
        