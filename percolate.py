import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx

def neig_ls(idx, n):
    cx = idx%n
    cy = idx//n
    nx = list([cx - 1, cx + 1])
    ny = list([cy - 1, cy + 1])
    nxn = [ele for ele in nx if ele >= 0 and ele < n]
    nyn = [ele for ele in ny if ele >= 0 and ele < n]
    out = []
    for i in nxn:
        ij = i + cy*n
        out.append(ij)
    for j in nyn:
        ij = cx + j*n
        out.append(ij)
    return out

def project(arr, n):
    zz = np.zeros((n, n))
    for idx in range(len(arr[0])):
        x = idx%n
        y = idx//n
        zz[y][x] = arr[0][idx]
    return zz

def num_cluster(prob, N):
    bonding = [] # This stores all bonded configs
    size = N**2
    for i in range(size):
        nei = neig_ls(i, N)
        for j in nei:
            rand = random.random()
            if rand < prob:
                if [j, i] not in bonding:
                    bonding.append([i, j])
    return bonding

def gen_G(N, bonding):
    # Generate a graph G
    G = nx.Graph()
    size = N**2
    for i in range(size):
        G.add_node(i)
    for i in bonding:
        G.add_edge(i[0],i[1])
    return G

def color_assign(G, N):
    # 0 indicates a blocked site
    # 1 indicates an empty site
    # 2 indicates a filled site
    nn = np.ones((1, N**2))
    big_cluster = list(nx.connected_components(G))
    if len(big_cluster) == 0:
        # all grid points are connected
        nn = nn*2
    else:
        ll = [len(i) for i in big_cluster]
        lmax = max(ll)
        for j in big_cluster:
            if len(j) == lmax:
                lmax = lmax + 1 # this is to prevent multiple cnt
                for k in j:
                    nn[0][k] = nn[0][k] + 1
            elif len(j) == 1:
                jj = list(j)[0]
                nn[0][jj] = nn[0][jj] - 1
    return nn

def run(prob, N):
    bonding = num_cluster(prob/2, N)
    G = gen_G(N, bonding)
    big_cluster = list(nx.connected_components(G))
    arr = color_assign(G, N)
    return arr

def perco_prob(prob, N, iters):
    k = 0
    l = 0
    while k < iters:
        k = k + 1
        arr = run(prob, N)
        mat = project(arr, N)
        if 2 in mat[0] and 2 in mat[-1]:
            l = l + 1
    return l/k

def clrmap(mat):
    cvals  = [0, 1, 2]
    colors = [(0, 0, 0), (0.4, 0.4, 0.4), (0.372549, 0.596078, 1)]
    norm = plt.Normalize(min(cvals), max(cvals))
    tuples = list(zip(map(norm,cvals), colors))
    cmap = LinearSegmentedColormap.from_list("", tuples)
    plt.imshow(mat, cmap=cmap, vmin=0, vmax=2)
    plt.show()

N = 20
#prob = 0.6
#arr = run(prob, N)
#mat = project(arr, N)
#print(perco_prob(prob, N, 100))
perco_doc = []
prob_ls = list(np.linspace(0, 1, 20))
for prob in np.linspace(0, 1, 20):
    perco_doc.append(perco_prob(prob, N, 200))

#print(perco_doc)
plt.figure()
plt.plot(prob_ls, perco_doc)
plt.xlabel('Average site occupation probability')
plt.ylabel('Percolation probability')
plt.show()
