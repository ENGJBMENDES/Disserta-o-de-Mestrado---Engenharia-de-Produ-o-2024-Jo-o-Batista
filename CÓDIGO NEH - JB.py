def NEH(caminho):

    def makespan(pij,n,m,seq):
        cij, cij[0][0] = [[0 for k in range(m)] for j in range(n)], pij[seq[0]][0]
        
        for j in range(1,m):
            cij[0][j] = cij[0][j-1] + pij[seq[0]][j]
        
        for i in range(1,n):
            cij[i][0] = cij[i-1][0] + pij[seq[i]][0]
            
            for j in range(1,m):
                cij[i][j] = max(cij[i-1][j], cij[i][j-1]) + pij[seq[i]][j]

        return cij

    f = open(caminho, 'r')

    linhas = f.readlines()
    n, m = map(int, linhas[0].split())

    pij=[]
    for i in range(1, n + 1):
        linha = linhas[i].strip()
        pij.append(list(map(int, linha.split())))

    for linha in pij:
        del linha[::2]

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
    for i in range(1, n):
        min_cmax = float('inf')

        for j in range(0, i + 1):
            seq_temp = seq_atual[:]
            seq_temp.insert(j,seq[i])
            cmax_temp = makespan(pij,len(seq_temp),m,seq_temp)[-1][-1]
            if min_cmax > cmax_temp:
                best_seq = seq_temp
                min_cmax = cmax_temp
        seq_atual = best_seq

    mk = makespan(pij,n,m,seq_atual)
    return seq_atual, mk[-1][-1]