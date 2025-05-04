import re

var = []
ind = {}

terminal = []
rules = []

i = 0
with open("grammar.txt", "r") as f:
    for line in f:
        line = line.strip().split()

        vu = line[0]
        if vu not in ind:
            print(vu)
            ind[vu] = i
            i = i + 1
            var.append(vu)

        u = ind[vu]
        if len(rules) <= u:
            rules.append([])

        rules[u].append(line[2:])

        for vv in set(line[2:]):
            if vv not in ind:
                ind[vv] = i
                i = i + 1
                var.append(vv)

            v = ind[vv]

            rules[u].append(v)

print(var)
print(ind)
print(rules)
