import re 
import copy 
from prettytable import PrettyTable as Table
 
# Read input from the file 
with open('input7.txt', 'r') as file: 
    input_string = file.read() 
 
# Split the input into lines for lexical analysis 
program = input_string.split('\n') 
 
# Tokens and their corresponding types 
 
# Operators 
operators = {'=': 'Assignment op', '+': 'Addition op', '-': 'Subtraction op', '>': 'Comparison op', '/': 'Division op', '*': 
'Multiplication op', '++': 'Increment op', '--': 'Decrement op'} 
optr_keys = operators.keys() 
 
# Comments 
comments = {r'//': 'Single Line Comment', r'/*': 'Multiline Comment Start', r'*/': 'Multiline Comment End', '/**/': 'Empty Multiline comment'} 
comment_keys = comments.keys()
# Header 
header = {'.h': 'header file'} 
header_keys = header.keys() 
sp_header_files = {'<stdio.h>': 'Standard Input Output Header', 
'<string.h>': 'String Manipulation Library'} 
 
# Macros 
macros = {r'#\w+': 'macro'} 
macros_keys = macros.keys() 
 
# Datatypes 
datatype = {'int': 'Integer', 'float': 'Floating Point', 'char': 
'Character', 'long': 'long int'} 
datatype_keys = datatype.keys() 
 
# Keywords 
keyword = {'return': 'keyword that returns a value from a block'} 
keyword_keys = keyword.keys() 
 
# Delimiters 
delimiter = {';': 'terminator symbol semicolon (;)'} 
delimiter_keys = delimiter.keys() 
# While blocks 
while_block = {'while': 'Enter While Loop', 'end while': 'Exit While Loop'} 
while_block_keys = while_block.keys() 
 
# Blocks 
blocks = {'begin': 'Enter Block', 'end': 'Exit Block\n\nTokens generated successfully'} 
block_keys = blocks.keys() 
 
# Builtin Functions 
builtin_functions = {'printf': 'printf prints its argument on the console'} 
 
# Non-Identifier Tokens 
non_identifiers = ['_', '-', '+', '/', '*', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '=', '|', '"', ':', ';', '{', '}', '[', ']', '<', '>', '?', '/'] 
 
# Numerals 
numerals = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
# Flags and Symbol Definitions 
dataFlag = False 
start_symbol = 'S' 
id = '' 
 
# Grammar Definitions 
 
# Rules of the Grammar 
rules = [] 
nonterm_userdef = [] 
term_userdef = [] 
 
# Dictionary to store grammar rules 
diction = {} 
firsts = {} 
follows = {} 
count = 0 
 
def print_table(header, data):
    table = Table(header) 
    for row in data: 
        table.add_row(row) 
    print(table) 

def construct_grammar():
    global rules, nonterm_userdef, term_userdef, id 
    rules = [ "S -> T M B A D", "T -> int", 
        "M -> main()", 
        "B -> begin", 
        "D -> end", 
        "A -> E W X", 
        "E -> T "+id+" = 1 ;", 
        "W -> while ( C ) P Q R | #", 
        "C -> n > 1", 
        "P -> "+id+" = "+id+" + 1 ;", 
        "Q -> n = n / 2 ;", 
        "R -> end while", 
        "X -> return "+id +" | #" 
    ]
    nonterm_userdef = ['S', 'T', 'M', 'B', 'D', 'A', 'E', 'W', 'P', 'Q', 'R', 'X', 'C'] 
    term_userdef = [id, 'n', 'int', 'main()', 'end', 'while', 'begin', '(', ')', '+', '/', 'end while', 'return', '1', '2', '>', '=', '0', ';']
def lexicalAnalyzer():
    global operators, optr_keys, comments, comment_keys, header, header_keys, macros, macros_keys, datatype, datatype_keys, keyword, keyword_keys, delimiter, delimiter_keys, while_block, while_block_keys, blocks, block_keys, builtin_functions, non_identifiers, numerals, dataFlag, id, count
    # Loop through each line of the program 
    for line in program: 
        count = count + 1 
        print('\033[1m' + "Line #", count, line + '\033[0m') 
        tokens = line.split(' ') 
        # Special case handling for 'end while' token 
        if 'end' in tokens and 'while' in tokens: 
            tokens = ['end while']
    # Remove empty tokens 
        while '' in tokens: 
            tokens.remove('') 
 
        print("Tokens are", tokens) 
        print('Properties:') 
        for token in tokens: 
            if '\r' in token: 
                position = token.find('\r') 
                token = token[:position] 
 
            if token in while_block_keys: 
                print(while_block[token]) 
            if token in block_keys: 
                print(blocks[token]) 
            if token in optr_keys: 
                print("Operator is: ", operators[token]) 
            if token in comment_keys: 
                print("Comment Type: ", comments[token]) 
            if token in macros_keys: 
                print("Macro is: ", macros[token]) 
            if '.h' in token: 
                print("Header File is: ", token, sp_header_files[token]) 
            if '()' in token: 
                print("Function named", token) 
            if dataFlag == True and (token not in non_identifiers) and ('()' not in token) and (token not in numerals): 
                print("Identifier: ", token) 
            if token in numerals: 
                print("Numeral: ", token) 
            if token in datatype_keys: 
                print("Type is: ", datatype[token]) 
                dataFlag = True 
            if token in keyword_keys: 
                print(keyword[token]) 
            if token in delimiter:
                print("Delimiter", delimiter[token]) 
            if '#' in token: 
                match = re.search(r'#\w+', token) 
                print("Header", match.group()) 
            if token in numerals: 
                print(token, type(int(token))) 
            if token not in optr_keys and token not in comment_keys and token not in macros_keys and token not in header_keys and token not in datatype_keys and token not in keyword_keys and token not in delimiter_keys and token not in while_block_keys and token not in block_keys and token not in non_identifiers and token not in numerals: 
                id = token 
        dataFlag = False 
        print() 
                
def first(rule): 
     global rules, nonterm_userdef, term_userdef, diction, firsts
     stack = [rule] 
     result = [] 
     while stack: 
        current_rule = stack.pop(0) 
 
        if len(current_rule) != 0 and (current_rule is not None): 
            # If the first character of the rule is a terminal, add it to the result. 
            if current_rule[0] in term_userdef: 
                result.append(current_rule[0]) 
            # If epsilon is encountered, add it to the result. 
            elif current_rule[0] == '#': 
                result.append('#') 
 
        if len(current_rule) != 0:
              if current_rule[0] in list(diction.keys()): 
                # If the current symbol is a non-terminal, expand its rules. 
                rhs_rules = diction[current_rule[0]] 
                for itr in rhs_rules: 
                    stack.insert(0, itr) 
 
                # If epsilon is not in the result, continue; otherwise, remove epsilon and proceed. 
                if '#' not in result: 
                    continue 
                else: 
                    result.remove('#') 
                    if len(current_rule) > 1: 
                        # Recursively compute FIRST for the remaining part of the rule. 
                        ans_new = first(current_rule[1:]) 
                        if ans_new is not None: 
                            if type(ans_new) is list: 
                                result += ans_new 
                            else: 
                                result += [ans_new] 
                        else: 
                            continue 
                    else: 
                        # If the rule is fully processed, add epsilon back to the result. 
                        result.append('#') 
 
     return result
def follow(nt):
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows 
    stack = [nt] 
    solset = set() 
    processed = set()
    while stack: 
        current_nt = stack.pop() 
        if current_nt == start_symbol:
              solset.add('$') 
        if current_nt not in processed: 
            processed.add(current_nt) 
 
            for curNT in diction: 
                rhs = diction[curNT] 
                for subrule in rhs: 
                    if current_nt in subrule: 
                        index_nt = subrule.index(current_nt) 
                        subrule = subrule[index_nt + 1:] 
 
                        while subrule and subrule[0] in term_userdef: 
                            solset.add(subrule[0]) 
                            break 
 
                        if not subrule:
                            stack.append(curNT) 
                        elif subrule[0] in nonterm_userdef: 
                            stack.append(subrule[0]) 
 
    return list(solset)
def computeAllFirsts():
    global rules, nonterm_userdef, term_userdef, diction, firsts 
    for rule in rules: 
        k = rule.split("->") 
        k[0] = k[0].strip() 
        k[1] = k[1].strip()
        rhs = k[1] 
        multirhs = rhs.split('|') 
        for i in range(len(multirhs)): 
            multirhs[i] = multirhs[i].strip() 
            multirhs[i] = multirhs[i].split() 
        diction[k[0]] = multirhs 
 
    print(f"\nRules: \n") 
    for y in diction: 
        production = '' 
        for x in diction[y]: 
            production += f"{' '.join(x)} | " 
        production = production[:-2] 
        print(f"{y} -> {production}") 
    print() 
 
    for y in list(diction.keys()): 
        t = set() 
        for sub in diction.get(y): 
            res = first(sub) 
            if res != None: 
                if type(res) is list: 
                    for u in res: 
                        t.add(u) 
                else: 
                    t.add(res) 
        firsts[y] = t 
 
    print("\nCalculated firsts:\n") 
    key_list = list(firsts.keys()) 
    index = 0 
    for gg in firsts: 
        print(f"first({key_list[index]}) => {firsts.get(gg)}") 
        index += 1 
    print()
def computeAllFollows():
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows 
    for NT in diction:
        solset = set() 
        sol = follow(NT) 
        if sol is not None: 
            for g in sol: 
                solset.add(g) 
        follows[NT] = solset
    print("\nCalculated follows:\n") 
    key_list = list(follows.keys()) 
    index = 0 
    for gg in follows: 
        print(f"follow({key_list[index]}) => {follows[gg]}") 
        index += 1 
    print()
def createParseTable():
    global diction, firsts, follows, term_userdef 
    print("\nFirsts and Follow Result table:\n")
    mx_len_first = max(len(str(firsts[u])) for u in diction) 
    mx_len_fol = max(len(str(follows[u])) for u in diction)
    print_table(['Non-Terminal', 'FIRST', 'FOLLOW'], [[u, 
str(firsts[u]), str(follows[u])] for u in diction]) 
    print() 
    ntlist = list(diction.keys()) 
    terminals = copy.deepcopy(term_userdef)
    remove_symbols = ['(', ')', '+', '/', '=', '1', '2', '0', ';', '>', 'end while'] 
    for symbol in remove_symbols:
         terminals.remove(symbol) 
    terminals.append('$') 
 
    mat = [['' for _ in terminals] for _ in ntlist] 
    grammar_is_LL = True 
 
    # Fill in the LL(1) parsing table. 
    for lhs in diction: 
        rhs = diction[lhs] 
        for y in rhs: 
            res = first(y)
              # Handle epsilon in FIRST set by combining FOLLOW set. 
            if '#' in res: 
                if type(res) == str: 
                    firstFollow = [res] 
                    fol_op = follows[lhs] 
                    if type(fol_op) == str: 
                        firstFollow.append(fol_op) 
                    else: 
                        firstFollow.extend(fol_op) 
                    res = firstFollow 
                else: 
                    res.remove('#') 
                    res.extend(follows[lhs]) 
 
            ttemp = [] 
            if type(res) is str: 
                ttemp.append(res) 
                res = copy.deepcopy(ttemp) 
 
            for c in res: 
                xnt = ntlist.index(lhs) 
                yt = terminals.index(c) 
                if mat[xnt][yt] == '': 
                    mat[xnt][yt] += f"{lhs}->{' '.join(y)}" 
                else: 
                    if f"{lhs}->{y}" in mat[xnt][yt]: 
                        continue 
                    else: 
                        grammar_is_LL = False 
                        mat[xnt][yt] += f",{lhs}->{' '.join(y)}" 
    print("\nGenerated parsing table:\n")
    print_table(['Non-Terminal', *terminals], [[ntlist[i], *mat[i]] for 
i in range(len(ntlist))]) 
    print() 
 
    return mat, terminals, grammar_is_LL
def validateStringUsingStackBuffer(parsing_table, grammarll1, table_term_list, input_string, term_userdef, start_symbol): 
    print("\nValidate String:\n") 
 
    if not grammarll1: 
        return f"\nInput String = \"{input_string}\"\nGrammar is not LL(1)" 
 
    stack = [start_symbol, '$'] 
    buffer = [] 
    input_string = input_string.split() 
    input_string.reverse() 
    buffer = ['$'] + input_string 
    parsingSteps = [] 
 
    while True: 
        if stack == ['$'] and buffer == ['$']: 
            parsingSteps.append([copy.deepcopy(' '.join(buffer)), copy.deepcopy(' '.join(stack)), "Valid"]) 
            result = "\nValid String!" 
            return result, parsingSteps 
        elif stack[0] not in term_userdef: 
            x = list(diction.keys()).index(stack[0]) 
            y = table_term_list.index(buffer[-1]) 
            if parsing_table[x][y] != '': 
                entry = parsing_table[x][y] 
                parsingSteps.append([copy.deepcopy(' '.join(buffer)), copy.deepcopy(' '.join(stack)), copy.deepcopy(entry)]) 
                lhs_rhs = entry.split("->") 
                lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip() 
                entryrhs = lhs_rhs[1].split() 
                stack = entryrhs + stack[1:] 
            else: 
                result = f"\nInvalid String! No rule at Table[{stack[0]}][{buffer[-1]}]." 
                return result, parsingSteps 
        else:
            if stack[0] == buffer[-1]: 
                parsingSteps.append([copy.deepcopy(' '.join(buffer)), copy.deepcopy(' '.join(stack)), f"Matched:{stack[0]}"])
                buffer = buffer[:-1] 
                stack = stack[1:] 
            else: 
                result = "\nInvalid String! Unmatched terminal symbols" 
                return result, parsingSteps
if __name__ == "__main__": 
    lexicalAnalyzer() 
    construct_grammar() 
    computeAllFirsts() 
    computeAllFollows() 
    mat, terminals, grammar_is_LL = createParseTable() 
    result, parsingSteps = validateStringUsingStackBuffer( 
        parsing_table=mat, 
        grammarll1=grammar_is_LL, 
        table_term_list=terminals, 
        input_string=input_string, 
        term_userdef=term_userdef, 
        start_symbol=start_symbol 
    ) 
    print_table(['Input', 'Stack', 'Action'], parsingSteps) 
    print() 
    print(result)