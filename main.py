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


def assemblyGenerator(token, assembly):
    pile = []

    recorder = 0
    label_id = 0

    results = []
    memory = 0

    for type, value in token:
        if type == "NUMBER":
            rec = "R" + str(recorder)
            assembly.append("MOV " + rec + ", #" + str(value))
            pile.append(rec)
            recorder += 1

        elif type == "OP":
            b = pile.pop()
            a = pile.pop()

            if value == "+":
                assembly.append("ADD " + a + ", " + a + ", " + b)
            elif value == "-":
                assembly.append("SUB " + a + ", " + a + ", " + b)
            elif value == "*":
                assembly.append("MUL " + a + ", " + a + ", " + b)
            elif value == "/":
                assembly.append("SDIV " + a + ", " + a + ", " + b)
            elif value == "%":
                assembly.append("MOD " + a + ", " + a + ", " + b)
            elif value == "^":
                label_id += 1
                loop_label = f"loop_{label_id}"
                end_label = f"end_{label_id}"

                resultado = f"R{recorder}"
                recorder += 1

                # resultado = base (a)
                assembly.append(f"MOV {resultado}, {a}")

                # expoente-- (b = b - 1)
                assembly.append(f"SUB {b}, {b}, #1")

                # loop
                assembly.append(f"{loop_label}:")
                assembly.append(f"CMP {b}, #0")
                assembly.append(f"BEQ {end_label}")
                assembly.append(f"MUL {resultado}, {resultado}, {a}")
                assembly.append(f"SUB {b}, {b}, #1")
                assembly.append(f"B {loop_label}")
                assembly.append(f"{end_label}:")

                pile.append(resultado)
                continue
            elif value == "//":
                assembly.append("SDIV " + a + ", " + a + ", " + b)

            pile.append(a)

        elif type == "MEM":
            if pile:
                value = pile.pop()
                assembly.append("MOV R_MEM, " + value)
                memory = "R_MEM"
            else:
                pile.append(memory)

    return assembly


archive = sys.argv[1]

assembly = []

with open(archive, "r") as f:
    for line in f:
        print(line.strip())
        token = tokenGenerator(line.strip())
        assemblyGenerator(token, assembly)
        print(token)
