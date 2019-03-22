
def parse_tab(tab):
    cut_list = []

    del_same(tab)
    print("before: ", tab)
    not_assigned(tab)
    print("after: ", tab)

def del_same(tab):      #   Delete same line in tab
	for	val,second in enumerate(tab):
		for first in tab[val + 1:]:
			if first == second:
				tab.remove(first)

def checkTwoSide(string):       #   Split the string at the delimiter
    #   splitAffectation used to contain first and last part of string. toFind used like delimiter
    splitAffectation = toFind = ""
    #   Use like a falg variable
    whichCase = 0

    toFind = "=>" if string.find("<=>") == -1 else "<=>"
    splitAffectation = string.split(toFind)
    for i in splitAffectation:
        whichCase = missingBracket(i)
        if whichCase == 1:
	    error_case("Error: Missing bracket in [" + string + ']')
        elif whichCase == 2:
	    error_case("Error: Missing a ')' bracket in [" + string + ']')
        elif whichCase == 3:
	    error_case("Error: Missing a '(' bracket in [" + string + ']')
    return 0

def not_assigned(tab):      #	Check if there are a good assignation expression
    test = 0
    for lineOfArray in tab:
        if not checkTwoSide(lineOfArray):
            for eatchChar in operand_n:
                if eatchChar in lineOfArray and eatchChar not in ['(', ')']:
                    lineOfArray.strip()
                    #print lineOfArray

def missingBracket(string):     #   Check if missing bracket in string
    #	Use to find multiple pair bracket
    counterBracket = 0 

    for i in string:
        if i == '(':
            counterBracket += 1
        elif i == ')':
            counterBracket -= 1
    if counterBracket:
        return 2 if counterBracket > 0 else 3
    return bracketBadFormat(string)

def bracketBadFormat(string):       #   Check if open bracket is before close bracket
    #	Flag to know if steps are pass
    flag = 0

    for i in string:
        if i in ['(', ')']:
            if i == ')' and not (flag & 1):
                error_case("Error: Declaration of '" + i +
                "' bracket before '(' in [" + i + "]")
            flag |= (1 << 0 if i == '(' else 1 << 1)
    return 0 if (flag & 1) and (flag & 2) or not flag else 1