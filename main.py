import sys


def initialState(line, i, tokens):

    char = line[i]

    if char == " ":
        return initialState, i + 1

    if char.isdigit():
        return numberState, i

    if char in ['+', '-', '*', '/', '%', '^']:

        if char == '/' and line[i + 1] == '/':
            tokens.append(("OP", "//"))
            return initialState, i + 1

        tokens.append(("OP", char))
        return initialState, i + 1

    if char == '(':
        tokens.append(("LPARENT", char))
        return initialState, i + 1

    if char == ')':
        tokens.append(("RPARENT", char))
        return initialState, i + 1

    if char.isalpha():
        return wordState, i


def numberState(line, i, tokens):
    num = ""

    while line[i] != " ":
        num += line[i]
        i += 1

    tokens.append(("NUMBER", num))

    return initialState, i


def wordState(line, i, tokens):
    word = ""

    while line[i].isalpha():
        word += line[i]
        i += 1

    if word == "RES":
        tokens.append(("RES", word))
    elif word == "MEM":
        tokens.append(("MEM", word))
    else:
        print("Palavra desconhecida!")

    return initialState, i


def tokenGenerator(line):
    tokens = []
    state = initialState
    i = 0

    while i < len(line):
        state, i = state(line, i, tokens)

    return tokens


archive = sys.argv[1]

with open(archive, "r") as f:
    for line in f:
        print(line.strip())
        token = tokenGenerator(line.strip())
        print(token)
