# LL(1) Parser

This project implements a basic **LL(1) parser** that reads a context-free grammar, computes FIRST and FOLLOW sets, builds a parsing table, and parses input strings according to the table.

## 📄 Grammar Format

The grammar must be defined in a plain text file with the following format:

- The initial variable must be at the top (left-handside of production)
- Each production is written on a separate line.
- The **left-hand side** (non-terminal) is followed by `->`.
- Multiple productions for the same non-terminal must be in separate lines.
- The **epsilon symbol** (empty string) is represented by `ε` (U+03B5).
- Terminals, non-terminals, `->` and `ε` are separated by spaces.

### ✅ Example:

```text
P -> L
L -> S Lp
Lp -> ; L
Lp -> ε
S -> id = E
S -> print ( E )
E -> T Ep
Ep -> + E
Ep -> - E
Ep -> ε
T -> F Tp
Tp -> * T
Tp -> / T
Tp -> ε
F -> id
F -> num
F -> ( E )
```

## 📁 File Locations

- **Grammar file:** 
    - By default, the parser reads the grammar from `grammar.txt` located in the current working directory.
    - This behaviour can be changed by modifying the value of the `grammarFile` variable.

- **Input strings:** 
    - Read from a file named `input.txt`.
    - This behaviour can be changed by modifying the value of the `inputFile` variable.

- **Parsing table / debug info:** 
    - Generated file `table.txt` (LL(1) table) in the current directory.
    - Generated file `production.txt` (string derivation) in the current directory.

## 🚀 How to Run

```bash
python3 main.py
```
