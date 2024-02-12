def NEHTRB(caminho):

    f = open(caminho, 'r')

    linhas = f.readlines()
    n, m = map(int, linhas[0].split())

    pij=[]
    for i in range(1, n + 1):
        linha = linhas[i].strip()
        pij.append(list(map(int, linha.split())))

    for linha in pij:
        del linha[::2]

    set=[]
    setup = [[[0 for j in range(n)] for j in range(n)] for k in range(m)]

    for i in range(n + 1, len(linhas)):
        linha = linhas[i].strip()
        if 'S' not in linha and 'M' not in linha:
            set.append(list(map(int, linha.split())))

    i = 0
    for k in range(m):
        for j in range(n):
            setup[k][j] = set[i]
            i = i + 1

    f.close()
    
    def makespan(pij,setup,n,m,seq):
        
        cij, cij[0][0] = [[0 for k in range(m)] for j in range(n)], pij[seq[0]][0]
        for k in range(1,m):
            cij[0][k] = cij[0][k-1] + pij[seq[0]][k]
        for j in range(1,n):
            cij[j][0] = cij[j-1][0] + setup[0][seq[j-1]][seq[j]] + pij[seq[j]][0]
            for k in range(1,m):
                if cij[j-1][k] + setup[k][seq[j-1]][seq[j]] >= cij[j][k-1]:
                    cij[j][k] = cij[j-1][k] + setup[k][seq[j-1]][seq[j]] + pij[seq[j]][k]
                elif cij[j-1][k] + setup[k][seq[j-1]][seq[j]] < cij[j][k-1]:
                    cij[j][k] = cij[j][k-1] + pij[seq[j]][k]

        return cij

    def mk_e(pij,setup,m,seq,j):
        
        if j == 0:
            e[0][0] = pij[seq[0]][0]
            for i in range(1,m):
                e[i][0] = e[i-1][0] + pij[seq[0]][i]
        else:
            e[0][j] = e[0][j-1] + setup[0][seq[j-1]][seq[j]] + pij[seq[j]][0]
            for i in range(1,m):
                e[i][j] = max(e[i-1][j], e[i][j-1] + setup[i][seq[j-1]][seq[j]]) + pij[seq[j]][i]


    def mk_q(pij,setup,n,m,seq,j):
        
        if j == n-1:
            q[m-1][n-1] = pij[seq[n-1]][m-1]
            for i in range(m-2,-1,-1):
                q[i][j] = q[i+1][j] + pij[seq[j]][i]
        else:
            q[m-1][j] = q[m-1][j+1] + setup[m-1][seq[j]][seq[j+1]] + pij[seq[j]][m-1]
            for i in range(m-2,-1,-1):
                q[i][j] = max (q[i+1][j], q[i][j+1] + setup[i][seq[j]][seq[j+1]]) + pij[seq[j]][i]


    def mk_f(pij,setup,m,seq,j):

        if j == 0:
            f[0][j] = pij[seq[j]][0]
            for i in range(1,m):
                f[i][j] = f[i-1][j] + pij[seq[j]][i]

        else:
            f[0][j] = e[0][j-1] + setup[0][seq[j-1]][seq[j]] + pij[seq[j]][0]
            for i in range(1,m):
                f[i][j] = max(f[i-1][j], e[i][j-1] + setup[i][seq[j-1]][seq[j]]) + pij[seq[j]][i]

    def greedy_f(setup,n,m,seq,j):
        
        mk_row = []
        
        if j < n-1:
            for i in range(m):
                mk = f[i][j] + setup[i][seq[j]][seq[j+1]] + q[i][j]
                mk_row.append(mk)    

        if j == n-1:
            for i in range(m):
                mk = f[i][j]
                mk_row.append(mk)
        
        return mk_row


    setup = [[[0 for j in range(n)] for j in range(n)] for k in range(m)]

    i = 0
    for k in range(m):
        for j in range(n):
            setup[k][j] = set[i]
            i = i + 1

    Ti, linha = [], 0
    for p in pij:
        a=[sum(p),linha]
        Ti.append(a)
        linha+=1

    Ti.sort(reverse=True)

    seq = []
    for i in range(n):
        seq.append(Ti[i][1])

    seq_atual = [seq[0]]

    for i in range(1, 2):
        min_cmax = float('inf')

        for j in range(0, i + 1):
            seq_temp = seq_atual[:]
            seq_temp.insert(j,seq[i])
            mk = makespan(pij,setup,len(seq_temp),m,seq_temp)
            cmax_temp = mk[-1][-1]
            if min_cmax > cmax_temp:
                best_seq = seq_temp
                min_cmax = cmax_temp
        seq_atual = best_seq

    for i in range(2,n):
        e = [[0 for j in range(len(seq_atual))] for i in range(m)]
        q = [[0 for j in range(len(seq_atual))] for i in range(m)]
        f = [[0 for j in range(len(seq_atual) + 1)] for i in range(m)]
        G = []
        
        for j in range(len(seq_atual)):
            mk_e(pij,setup,m,seq_atual,j)
        
        for j in range(len(seq_atual)-1,-1,-1):
            mk_q(pij,setup,len(seq_atual),m,seq_atual,j)

        for j in range(0, i + 1):
            seq_temp = seq_atual[:]
            seq_temp.insert(j,seq[i])
            mk_f(pij,setup,m,seq_temp,j)

        for j in range(0, i + 1):
            seq_temp = seq_atual[:]
            seq_temp.insert(j,seq[i])
            greedy = greedy_f(setup,len(seq_temp),m,seq_temp,j)
            G.append(greedy)

        mk = []
        for i in range(len(seq_temp)):
            mk.append([max(G[i]),i])
        
        minimo = min(mk)
        seq_atual.insert(minimo[1],seq[i])
    
    return seq_atual, minimo[0]

