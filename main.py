import re

# Globals
eps = "ε"
end = "$"

vars = set()
rules = {}
terminal = {}

src = ""

with open("grammar.txt", "r") as f:
    for line in f:
        line = line.strip().split()

        u = line[0]

        if src == "":
            src=u

        terminal[u] = False
        if u not in rules:
            rules[u]=[]
            vars.add(u)
        rules[u].append(line[2:])

        for v in set(line[2:]):
            if v not in rules:
                vars.add(v)
                if v not in terminal:
                    terminal[v] = True

# Debugging
print(vars)
print(rules)
print(terminal)

first = {}

for u in vars:
    if terminal[u]: 
        first[u]={u}

n = len(rules)

for i in range(n):
    for u, rs in rules.items():
        if u not in first:
            first[u]=set()

        for rule in rs:
            j = 0
            while j < len(rule):
                v = rule[j]
                if v not in first: break

                for w in first[v]:
                    first[u].add(w)
                if eps not in first[v]:
                    break
                j = j + 1
            if j == len(rule):
                first[u].add(eps)

# Debugging
print("FIRST:", first)

follow = {}
follow[src]={end}

for _, rs in rules.items():
    for rule in rs:
        j = 0
        while j + 1 < len(rule):
            [u, v] = [rule[j], rule[j + 1]]
            for w in first[v]:
                if w == eps: continue
                if u not in follow:
                    follow[u] = set()
                follow[u].add(w)
            j = j + 1

# Debugging
print("FOLLOW:", follow)
