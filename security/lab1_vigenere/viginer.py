import operator

def decode(k_len, text):
    blocks = []
    for i in range(k_len):
        blocks.append(''.join([text[j] for j in range(i,len(text),k_len)]))

    keyword = ''
    for block in blocks:
        block_freq = {}
        for letter in block:
            block_freq[letter] = block_freq[letter]+1 if letter in block_freq else 1
        block_freq = dict((letter, block_freq[letter]*100.0/len(block)) for letter in block_freq)
        #block_freq = sorted(block_freq.items(), key=operator.itemgetter(1), reverse=True)

        offsets = {}
        for offset in range(27):
            offsets[offset] = 0
            for letter in block:
                new_letter = ord(letter)-offset
                if new_letter > ord('z'): new_letter -= 26
                if new_letter < ord('a'): new_letter += 26
                new_letter = chr(new_letter)
                offsets[offset] += abs(block_freq[letter]-freq[new_letter])

        offsets = sorted(offsets.items(), key=operator.itemgetter(1))
        keyword += chr(offsets[0][0]+ord('a'))
    print keyword

    i = 0
    decoded_text = ''
    for letter in text:
        new_letter = ord(letter)-(ord(keyword[i])-ord('a'))
        if new_letter > ord('z'): new_letter -= 26
        if new_letter < ord('a'): new_letter += 26
        decoded_text += chr(new_letter)

        i+=1
        if i == len(keyword): i = 0

    print decoded_text
        
def factors(n):
    return set(reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def factors_add(div, n):
    d = 2
    while n > 1:
        if n % d == 0:
            div[d] = div[d] + 1 if d in div else 1
            n = n/d
        else:
            d += 1

#
#start here
#

freq = {}
with open('freq', 'r') as freq_file:
    for line in freq_file:
        letter, f = line.split()
        freq[letter.lower()] = float(f)

freq = dict(sorted(freq.items(), key=operator.itemgetter(1), reverse=True))
text = open('var1_encoding1.txt','r').read()

# div = {}

# for i in range(len(text)-2):
#     sample = text[i:i+3]
#     pos = [i for i in range(len(text)) if text.startswith(sample, i)]

#     if len(pos) > 1:
#         dlt = [pos[i+1]-pos[i] for i in range(len(pos)-1)]

#         for delta in dlt:
#             for x in factors(delta):
#                 div[x]=div[x]+1 if x in div else 1
#             #factors_add(div, delta)

# div = sorted(div.items(), key=operator.itemgetter(1), reverse=True)
# for x, v in div[0:20]:
#     print x, v

k_len = 8

d_text = decode(k_len, text)




