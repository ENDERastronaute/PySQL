

def advance(current_index, tokens):
    current_index += 1

    if current_index < len(tokens):
        current_token = tokens[current_index]

    else:
        current_token = None

    return current_token, current_index