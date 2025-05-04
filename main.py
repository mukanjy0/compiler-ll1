# Globals
eps = "ε"
end = "$"

vars = []
rules = {}
terminal = {}

src = ""

with open("grammar0.txt", "r") as f:
    for line in f:
        line = line.strip().split()

        u = line[0]

        if src == "":
            src=u

        terminal[u] = False
        if u not in rules:
            rules[u]=[]
            vars.append(u)
        rules[u].append(line[2:])

        for v in set(line[2:]):
            if v not in rules:
                vars.append(v)
                if v not in terminal:
                    terminal[v] = True

def unique(ls : list) -> list:
    aux = sorted(ls)
    res = []
    for i in range(len(aux)):
        if i > 0 and aux[i] == aux[i - 1]: continue
        res.append(aux[i])
    return res

vars = unique(vars)

# Debugging
print(vars)
print(rules)
print(terminal)

first = {}

N = 0
for u in vars:
    if terminal[u]: 
        first[u]={u}
    else:
        N = N + 1

n = len(rules)

for i in range(n):
    for u, rs in rules.items():
        if u not in first:
            first[u]=[]

        for rule in rs:
            j = 0
            while j < len(rule):
                v = rule[j]
                if v not in first: break

                for w in first[v]:
                    first[u].append(w)
                if eps not in first[v]:
                    break
                j = j + 1
            if j == len(rule):
                first[u].append(eps)

            first[u] = unique(first[u])

# Debugging
print("FIRST:", first)

follow = {}
follow[src]={end}

ind = {}
var = []
adj = [[] for _ in range(N)]

id = 0
for vr in vars:
    if terminal[vr]: continue
    ind[vr] = id
    var.append(vr)
    id = id + 1

for s, rs in rules.items():
    for rule in rs:
        j = 0
        while j + 1 < len(rule):
            [u, v] = [rule[j], rule[j + 1]]

            if not terminal[u]:
                for w in first[v]:
                    if w == eps: continue
                    if u not in follow:
                        follow[u] = []
                    follow[u].append(w)

            j = j + 1

        j = len(rule) - 1
        while j >= 0:
            v = rule[j]
            if eps not in first[v]: break
            if v != eps:
                adj[ind[s]].append(ind[v])
            j = j - 1

# Kosaraju
def kosaraju(G : list):
    n = len(G)
    vis = [False] * n
    postorder = []

    def dfs(u : int):
        if vis[u]: return
        vis[u] = True

        for v in G[u]:
            dfs(v)
        postorder.append(u)

    for u in range(n):
        dfs(u)

    postorder.reverse()

    G2 = [[] for _ in range(N)]
    for u in range(n):
        for v in G[u]:
            G2[v].append(u)

    vis = [0] * n

    def dfs2(u : int, p : int):
        if vis[u] > 0: return
        vis[u] = p

        for v in G[u]:
            dfs2(v, p)

    i = 1
    sccs = {}
    for u in postorder:
        if vis[u] == 0:
            dfs2(u, i)
            i = i + 1
        if vis[u] not in sccs:
            sccs[vis[u]] = []
        sccs[vis[u]].append(u)

    return sccs

sccs = kosaraju(adj)
varSccs = { k : [var[u] for u in v] for k, v in sccs.items()}
print()
print("SCCS:", varSccs)
print()

for u in range(N):
    adj[u] = unique(adj[u])

# Debugging
print("FOLLOW:", follow)
