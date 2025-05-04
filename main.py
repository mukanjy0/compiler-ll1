# Globals

grammarFile = "grammar.txt"
inputFile = "input.txt"

eps = "ε"
end = "$"

vars = []
rules = {}
terminal = {}

src = ""

with open(grammarFile, "r") as f:
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

follow = {}

ind = {}
var = []
adj = [[] for _ in range(N)]

id = 0
for vr in vars:
    if terminal[vr]: continue
    ind[vr] = id
    var.append(vr)
    follow[vr] = []
    id = id + 1

follow[src].append(end)

for s, rs in rules.items():
    for rule in rs:
        j = 0
        while j + 1 < len(rule):
            [u, v] = [rule[j], rule[j + 1]]

            if not terminal[u]:
                for w in first[v]:
                    if w == eps: continue
                    follow[u].append(w)

            j = j + 1

        j = len(rule) - 1
        while j >= 0:
            v = rule[j]
            if not terminal[v] and s != v:
                adj[ind[s]].append(ind[v])
            if eps not in first[v]: break
            j = j - 1

for vr in follow.keys():
    follow[vr] = unique(follow[vr])

for u in range(N):
    adj[u] = unique(adj[u])

vAdj = {}
for u in range(N):
    vAdj[var[u]]=[var[v] for v in adj[u]]
print(f"Adj: {vAdj}\n")

def toposort(G : list):
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
    return postorder

def kosaraju(G : list):
    order = toposort(G)

    G2 = [[] for _ in range(N)]
    for u in range(n):
        for v in G[u]:
            G2[v].append(u)

    vis = [0] * n

    def dfs(u : int, p : int):
        if vis[u] > 0: return
        vis[u] = p

        for v in G2[u]:
            dfs(v, p)

    i = 1
    sccs = {}
    for u in order:
        if vis[u] == 0:
            dfs(u, i)
            i = i + 1
        if vis[u] not in sccs:
            sccs[vis[u]] = []
        sccs[vis[u]].append(u)

    return sccs

sccs = kosaraju(adj)

cc = [0] * N
ncc = 1
for c, ls in sccs.items():
    for u in ls:
        cc[u]=c
        if ncc < c:
            ncc = c

follow2 = [[] for _ in range(ncc + 1)]
for c, ls in sccs.items():
    for u in ls:
        follow2[c].extend(follow[var[u]])

for u in range(1,ncc + 1):
    follow2[u] = unique(follow2[u])

adj2 = [[] for _ in range(ncc + 1)]
for u in range(N):
    for v in adj[u]:
        if cc[u] == cc[v] or cc[v] in adj2[cc[u]]:
            continue
        adj2[cc[u]].append(cc[v])

order = toposort(adj2)

for u in order:
    for v in adj2[u]:
        follow2[v].extend(follow2[u])

for u in range(1,ncc + 1):
    follow2[u] = unique(follow2[u])
    for v in sccs[u]:
        follow[var[v]] = follow2[u]

# Debugging
print(f"Vars:\n{vars}\n")
print(f"Rules:\n{rules}\n")
print(f"Terminal:\n{terminal}\n")

print(f"FIRST: {first}\n")

varSccs = { k : [var[u] for u in v] for k, v in sccs.items()}
print(f"\nSCCS: {varSccs}\n")

print(f"FOLLOW: {follow}\n")
 
for u in first:
    first[u] = set(first[u])

# Building predictive table
terminals = sorted([t for t, is_term in terminal.items() if is_term] + [end])
table = {A: {a: None for a in terminals} for A in rules}
for A, prods in rules.items():
    for prod in prods:
        first_alpha = set()
        for X in prod:
            first_alpha |= (first[X] - {eps})
            if eps in first[X]:
                continue
            else:
                break
        else:
            first_alpha |= set(follow.get(A, []))
        for a in first_alpha:
            table[A][a] = prod

# Rule EXTRACT
for A in table:
    for a in list(table[A].keys()):
        if table[A][a] is None and a in follow.get(A, []):
            table[A][a] = "EXTRACT"
    if table[A].get(end) is None:
        table[A][end] = "EXTRACT"
# Rule EXPLORE
for A in table:
    for a in table[A]:
        if table[A][a] is None:
            table[A][a] = "EXPLORE"

# Write table to table.txt
with open("table.txt", "w") as f:
    print("Predictive Parsing Table:", file=f)
    header = ['NT'] + terminals
    row_fmt = ''.join(["{:<12}" for _ in header])
    print(row_fmt.format(*header), file=f)
    for A in sorted(table.keys()):
        row = [A]
        for a in terminals:
            entry = table[A][a]
            if isinstance(entry, list):
                cell = ' '.join(entry) or eps
            else:
                cell = entry
            row.append(cell)
        print(row_fmt.format(*row), file=f)

# Step by step production
def parse_string(input_str):
    input_syms = input_str.split() + [end]
    stack = [end, src]
    i = 0
    with open("production.txt", "w") as f:
        print("\nParsing Steps:", file=f)
        print(f"{'Stack':<40}{'Input':<100}Action", file=f)
        while stack:
            print(f"{str(stack):<40}{str(input_syms[i:]):<100}", end='', file=f)
            top = stack.pop()
            a = input_syms[i]
            if terminal.get(top, False) or top == end:
                if top == a:
                    print(f"Match '{a}'", file=f)
                    i += 1
                    continue
                else:
                    print(f"Error: expected '{top}' but got '{a}'", file=f)
                    return False
            entry = table[top][a]
            if entry == "EXTRACT":
                print("Action: EXTRACT (pop nonterminal)", file=f)
                continue
            if entry == "EXPLORE":
                print(f"Action: EXPLORE (skip terminal '{a}' )", file=f)
                i += 1
                continue
            prod_str = ' '.join(entry)
            print(f"Output: {top} -> {prod_str}", file=f)
            for sym in reversed(entry):
                if sym != eps:
                    stack.append(sym)
        print("Success: ✅ Input accepted", file=f)

    return True

with open(inputFile, "r") as f:
    e = f.readline().strip()
    print("\nInput:", e)
    print("Result:", parse_string(e))
