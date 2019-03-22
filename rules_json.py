#put all the rules in a json.
#Exemple: 'E': ['=>', 'C']
#E is true if C is true
#cette fonction est plus sale qu'une souris de l'e1
def rules_json(tab):
    rules = {}
    implies = "=>"
    query = "?"
    facts = "="
    op_or = "|"
    op_and = "+"
    oups = "<"
    for line in tab:
        if implies in line:
            splitline = line.split("=>")
            splitline.reverse()
            if oups in splitline[1]:
                tmp = splitline[1]
                getrule = tmp[:-1]
                splitline[1] = getrule
            if op_or or op_and in splitline[0]:
                for var in splitline[0]:
                    if var.isalpha():
                        key = var
                        value = splitline[1]
                        rules[key] = value
            elif op_or or op_and not in splitline[0]:
                key = splitline[0]
                value = splitline[1]
                rules[key] = value
        elif query in line:
            query = line[1:]
        elif facts in line:
            knownfacts = line[1:]
    solver(rules, query, knownfacts)

def solver(rules, query, facts):
    print("rules: ", rules)
    print("query: ", query)
    print("facts: ", facts)