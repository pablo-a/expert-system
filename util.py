def get_two_by_two(some_list):
    for i in range(len(some_list) - 1):
        yield (some_list[i], some_list[i+1])


def get_three_by_three(some_list):
    for i in range(len(some_list) - 2):
        yield (some_list[i], some_list[i+1], some_list[i+2])

def print_list(some_list):
    string = "\t["
    for elem in some_list[:-1]:
        string += f"{elem}, "
    string += f"{some_list[-1]}]"
    return string