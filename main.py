import sys


def geradorToken(linha):
    tokens = []

    i = 0

    while i < len(linha):
        char = linha[i]

        if char == " ":
            i += 1
            continue

        if char.isdigit():
            num = ""

            while linha[i] != " ":
                num += linha[i]
                i += 1

            tokens.append(("NUMBER", num))
            continue

        if char in ['+', '-', '*', '/', '%', '^']:

            if char == '/' and linha[i + 1] == '/':
                tokens.append(("OP", "//"))
                i += 2
                continue

            tokens.append(("OP", char))
            i += 1
            continue

        if char == '(':
            tokens.append(("LPARENT", char))
            i += 1
            continue

        if char == ')':
            tokens.append(("RPARENT", char))
            i += 1
            continue

        if char.isalpha():
            word = ""

            while linha[i].isalpha():
                word += linha[i]
                i += 1

            if word == "RES":
                tokens.append(("RES", word))
            elif word == "MEM":
                tokens.append(("MEM", word))
            else:
                print("Palavra desconhecida!")

            continue

    return tokens


arquivo = sys.argv[1]

with open(arquivo, "r") as f:
    for linha in f:
        print(linha.strip())
        token = geradorToken(linha.strip())
        print(token)
