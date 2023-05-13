
####### Problem 3 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('elephant', 'relevant'), ('AAAGAATTCA', 'AAATCA')]
alignments = [('bo-o-k', 'b-a-ck'), ('kooka-bu-rr-a', 'kook-yb-i-rd-'), ('-elep-hant','rele-v-ant'), ('AAAGAATTCA', '--A-AA-TCA')]

def MED(S, T):
    if (S == ""):
        return(len(T))
    elif (T == ""):
        return(len(S))
    else:
        if (S[0] == T[0]):
            return(MED(S[1:], T[1:]))
        else:
            return(1 + min(MED(S, T[1:]), MED(S[1:], T)))


def fast_MED(S, T, MED={}):
    if (S, T) in MED:
        return MED[(S, T)]
    elif (S == ""):
        MED[(S, T)] = len(T)
    elif (T == ""):
        MED[(S, T)] = len(S)
    else:
        if (S[0] == T[0]):
            MED[(S, T)] = fast_MED(S[1:], T[1:], MED)
        else:
            MED[(S, T)] = 1 + min(fast_MED(S, T[1:], MED), fast_MED(S[1:], T, MED))
    return MED[(S, T)]

def fast_align_MED(S, T, MED={}):
    m = len(S)
    n = len(T)
    if m == 0:
        return '-' * n, T
    if n == 0:
        return S, '-' * m
    D = [[0 for j in range(n+1)] for i in range(m+1)]
    for i in range(1, m+1):
        D[i][0] = i
    for j in range(1, n+1):
        D[0][j] = j
    for j in range(1, n+1):
        for i in range(1, m+1):
            if S[i-1] == T[j-1]:
                D[i][j] = D[i-1][j-1]
            else:
                D[i][j] = min(D[i-1][j], D[i][j-1], D[i-1][j-1]) + 1
    i, j = m, n
    align_S = ''
    align_T = ''
    while i > 0 or j > 0:
        if i > 0 and j > 0 and S[i-1] == T[j-1]:
            align_S = S[i-1] + align_S
            align_T = T[j-1] + align_T
            i -= 1
            j -= 1
        elif i > 0 and D[i][j] == D[i-1][j] + 1:
            align_S = S[i-1] + align_S
            align_T = '-' + align_T
            i -= 1
        else:
            align_S = '-' + align_S
            align_T = T[j-1] + align_T
            j -= 1
    return align_S, align_T

def test_MED():
    for S, T in test_cases:
        assert fast_MED(S, T) == MED(S, T)
                                 
def test_align():
    for i in range(len(test_cases)):
        S, T = test_cases[i]
        align_S, align_T = fast_align_MED(S, T)
        assert (align_S == alignments[i][0] and align_T == alignments[i][1])
