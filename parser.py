from fact import Fact

def setup_engine_query(engine, input):
    for line in input:
        engine.add_query(line)

def setup_engine_facts(engine, input):
    for line in input:
        engine.add_facts(line)

def setup_engine_rules(engine, input):
    input_without_bi = handle_biconditional(engine, input)
    tokenized_input = cut_statement(input_without_bi)
    handle_operations_in_conclusion(engine, tokenized_input)
    parse_all_rules(engine, tokenized_input)

########################### BICONDITIONAL #####################################

def handle_biconditional(engine, input):
    for statement in input:
        if is_biconditional(statement):
            opposit_statement = reverse_statement(statement)
            # add opposit to input array.
            input.append(opposit_statement)

    # replace "<=>" by "=>" in all statements.
    input_without_bi = map(lambda x: x.replace("<=>", "=>"), input)
    return input_without_bi

def is_biconditional(statement):
    return True if "<=>" in statement else False

def reverse_statement(statement):
    splitted = statement.split(" <=> ")
    splitted.reverse()
    splitted_with_symbol = [splitted[0], "=>", splitted[1]]
    merged = " ".join(splitted_with_symbol)
    return merged

##################### SPLITTING RULES IN 2 ####################################

def cut_statement(input):
    tokenized_input = []
    for statement in input:
        if not " => " in statement:
            continue
        splitted = statement.split(" => ")
        rule = splitted[0]
        conclusion = splitted[1]
        new_statement = {"rule": rule, "conclusion": conclusion}
        tokenized_input.append(new_statement)
    return tokenized_input

######################## OPERATIONS IN CONCLUSION #############################

# TODO: Implement
def handle_operations_in_conclusion(engine, input):
    """
        "A + B" => ["A", "B"]
    """
    # TODO: Handle OR/XOR operations ?
    pass

###################### PARSING RULES ##########################################

def parse_all_rules(engine, input):
    for statement in input:
        conclusion_array = parse_conclusion(engine, statement['conclusion'])
        rule = parse_rule(statement['rule'])

        for conclusion in conclusion_array:
            engine.add_rule(conclusion, rule)

############### CONCLUSION ###############

# TODO: Implement
def parse_conclusion(engine, conclusions):
    "return an array of Fact from an array of conclusions"
    return []


############ PRIORITY #####################

# TODO: Implement
def parse_rule(rule):
    """
        Return a Fact or Operation insctance equivalent to the rule.
        Input : A + (B | C)
        Output : And(A, Or(B, C))
    """
    return []


