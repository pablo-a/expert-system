from fact import Fact
import operations
import util
import logging
import re

def setup_engine_query(engine, input):
    for line in input:
        engine.add_query(line)

def setup_engine_facts(engine, input):
    for line in input:
        engine.add_facts(line)

def setup_engine_rules(engine, input):
    logging.debug(f"SETUP ENGINE RULES\n")
    logging.debug(f"non parsed rules : {util.print_list(input)}")

    input_without_bi = handle_biconditional(engine, input)
    logging.debug(f"handle <=> : {util.print_list(input_without_bi)}")

    split_neg_operator = check_negative_operator(input_without_bi)
    logging.debug(f"Neg operator : {util.print_list(split_neg_operator)}")

    tokenized_input = cut_statement(split_neg_operator)
    parse_all_rules(engine, tokenized_input)

########################### BICONDITIONAL #####################################

def handle_biconditional(engine, input):
    for statement in input:
        if is_biconditional(statement):
            opposit_statement = reverse_statement(statement)
            # add opposit to input array.
            input.append(opposit_statement)

    # replace "<=>" by "=>" in all statements.
    input_without_bi = list(map(lambda x: x.replace("<=>", "=>"), input))
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

####################### CHECK NEGATIVE OPERATOR ###############################

def check_negative_operator(rules):
    new_rules = []
    for statement in rules:
        splitted = statement.split()
        for index, elem in enumerate(splitted):
            if re.match(r"\![a-zA-Z]$", elem):
                splitted[index:index+1] = ["!", elem[1]]
        joined = " ".join(splitted)
        new_rules.append(joined)
    return new_rules
                

###################### PARSING RULES ##########################################

def parse_all_rules(engine, input):
    for statement in input:
        logging.debug(f"Parsing Statement : {statement}")
        conclusion_array = parse_conclusion(engine, statement['conclusion'])
        rule = parse_rule(engine, statement['rule'])
        logging.debug(f"\n\tEND PARSING : {rule} => {conclusion_array}")

        for conclusion in conclusion_array:
            engine.add_rule(conclusion, rule)

############### CONCLUSION ###############

# TODO: Implement
def parse_conclusion(engine, conclusions):
    "return an array of Facts from conclusion"
    tokens = conclusions.split()
    convert_to_fact_instances(engine, tokens)
    if len(tokens) == 1:
        return tokens
    for token in tokens:
        pass
    return []


############ PRIORITY #####################

operation_priority = ["+", "|", "^"]
operation_classes  = [operations.And, operations.Or, operations.Xor]

def parse_rule(engine, rule):
    """
        Return a Fact or Operation insctance equivalent to the rule.
        Input : A + (B | C)
        Output : And(A, Or(B, C))
    """
    logging.debug(f"Parsing Rule : \"{rule}\"")

    tokens = rule.split()
    # literal to Object : "A" => Fact("A")
    convert_to_fact_instances(engine, tokens)
    logging.debug(f"Fact converted: {util.print_list(tokens)}")

    # remove parenthesis by simplifying content.
    tokens = parse_parenthesis(tokens)
    logging.debug(f"rm parenthesis : {util.print_list(tokens)}")

    # simplify rule while handling priority.
    rule = parse_operations_priority(tokens)
    if len(rule) == 1:
        logging.debug(f"parsed operations : {util.print_list(rule)}")
        return rule[0]
    logging.critical(f"rule before parsing : {util.print_list(rule)}\nrule after operation parsing : {util.print_list(rule)}")
    return []

def convert_to_fact_instances(engine, tokens):
    "Convert facts literals to instances of Fact"
    for index,elem in enumerate(tokens):
        if isinstance(elem, str) and elem.isalpha():
            tokens[index] = Fact(elem, engine)

def parse_parenthesis(rule):
    if not "(" in rule:
        return rule
    positions = []
    for index, token in enumerate(rule):
        if "(" in token:
            positions.append(index)
        elif ")" in token:
            closing_bracket = index
            break
    opening_bracket = positions.pop()
    rule[opening_bracket:closing_bracket+1] = parse_operations_priority(rule[opening_bracket, closing_bracket+1])
    # Tail recursion : simplify the simplified rule until no parenthesis.
    return parse_parenthesis(rule)

def parse_operations_priority(tokens):
    tokens = parse_negative(tokens)
    logging.debug(f"remove negation literals : {util.print_list(tokens)}")
    for operator, op_class in zip(operation_priority, operation_classes):
        tokens = parse_operator(operator, op_class, tokens)
    return tokens

def parse_operator(operator, op_class, rule):
    # No more operations.
    if len(rule) <= 2:
        return rule

    index = 0
    for left_token, middle_token, right_token in util.get_three_by_three(rule):
  
        if middle_token == operator:
            obj = op_class(left_token, right_token)
            rule[index:index+3] = [obj]
            return parse_operator(operator, op_class, rule)

        index += 1
 
    return rule

def parse_negative(rule):
    if len(rule) < 2:
        return rule

    index = 0
    for token, next_token in util.get_two_by_two(rule):
        if token == "!" and (isinstance(next_token, Fact) or issubclass(next_token, operations.Operator)):
            obj = operations.Not(next_token)
            rule[index:index+2] = [obj]
            return parse_negative(rule)
        index += 1

    return rule


