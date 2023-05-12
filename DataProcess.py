def String_split_nth(str_line, n):
    list_splited = [str_line[i:i + n] for i in range(0, len(str_line), n)]  # Split done here
    print(list_splited)
    return list_splited


def reshape_list(block, width):
    data = []
    for i in range(0, len(block), width):
        line = block[i:i + width]
        data.append(line)
    return data

def FormatData(string_char):
    return reshape_list(String_split_nth(string_char),128)