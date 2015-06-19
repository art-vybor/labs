match_award      = 10
mismatch_penalty = -5
gap_penalty      = -5

s1 = 'AGTA'
s2 = 'ATA'


def needle(s1, s2):
    def match(a, b): return match_award if a == b else mismatch_penalty

    m, n = len(s1), len(s2)
    
    F = []  #init table
    for x in range(m+1):
        F.append([])
        for y in range(n+1):
            F[-1].append(0)
   
    # fill the table
    for i in range(0, m + 1):
        F[i][0] = gap_penalty * i
    for j in range(0, n + 1):
        F[0][j] = gap_penalty * j
    for i in range(1, m + 1):
        for j in range(1, n+1):
            F[i][j] = max(F[i-1][j-1] + match(s1[i-1], s2[j-1]),
                          F[i-1][j] + gap_penalty,
                          F[i][j-1] + gap_penalty)

    # traceback
    align1, align2 = '', ''
    i,j = m,n
    while i > 0 and j > 0:
        if F[i][j] == F[i-1][j-1] + match(s1[i-1], s2[j-1]):
            align1 += s1[i-1]
            align2 += s2[j-1]
            i -= 1
            j -= 1
        elif F[i][j] == F[i-1][j] + gap_penalty:
            align1 += s1[i-1]
            align2 += '-'
            i -= 1
        elif F[i][j] == F[i][j-1] + gap_penalty:
            align1 += '-'
            align2 += s2[j-1]
            j -= 1

    while i > 0:
        align1 += s1[i-1]
        align2 += '-'
        i -= 1
    while j > 0:
        align1 += '-'
        align2 += s2[j-1]
        j -= 1
    print align1[::-1]
    print align2[::-1]

needle(s1, s2)