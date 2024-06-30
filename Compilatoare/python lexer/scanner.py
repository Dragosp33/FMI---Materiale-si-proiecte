import re

def scan(input_file):
    token_types = [
        ('IF', r'^if\b'),
        ('ELSE', r'^else\b'),
        ('COMP_OPERATOR', r'(==|!=|<=|>=|<|>)'),
        (r'[\&\|\^\~]', 'BITWISE_OP'),


        ('LEFT_BRACE', r'^{'),
        ('RIGHT_BRACE', r'^}'),
        ('SEMICOLON', r'^;'),
        ('ASSIGN', r'^='),
        ('LT', r'^<'),
        ('PLUS', r'^\+'),
        ('MINUS', r'^-'),


        ('IDENTIFIER', r'^[a-zA-Z_][a-zA-Z0-9_]*'),
        ('LEFT_PAREN', r'^\('),
        ('RIGHT_PAREN', r'^\)'),

        ( 'SPECIAL_CHARACTER', r'[\!!\@\$]'),
        ('MULTI_COMMENT', r'\"\"\"[\s\S]*?\"\"\"'),
        ('TIMES', r'^\*'),
        ('DIVIDE', r'^/'),
        ('INTEGER', r'^\d+'),

        ('PRINT', r'print'),
        ('COMMENT', r'\#.*'),
        ('SKIP', r'^.'),
        ('SPACE', r' '),
        ('NEWLINE', r'\n'),
        ('TAB', r'\t')

    ]
    tokens = []
    current_line = 1
    current_pos = 0
    current_token_len = 0
    prev_token = None
    with open(input_file, 'r') as f:
        input_text = f.read()
    while current_pos < len(input_text):
        match = None
        for token_type, pattern in token_types:
            regex = re.compile(pattern)
            match = regex.match(input_text[current_pos:])
            if match:
                token_value = match.group(0)
                #print("token: ", token_value, "prev: ", prev_token)

                if token_type != 'SPACE' and token_type != 'NEWLINE' and token_type != 'SKIP':

                    if prev_token == 'IF' or prev_token == 'ELSE':

                        if token_type != 'IDENTIFIER':

                            error_token = input_text[current_pos]
                            error_pos = current_pos
                            while error_token != ' ' and error_token != '\n' and error_token != '\t' and error_pos < len(
                                    input_text) - 1:
                                error_pos += 1
                                error_token = input_text[error_pos]
                            current_token_len = 0
                            print(error_token, token_type, token_value, current_line, current_pos, 'EROARE ')
                        else:
                            prev_token = token_type
                            print(
                                f"Value: {token_value}, Type: {token_type}, Length: {len(token_value)}, Line: {current_line}, Pointer: {current_pos}")
                    else:
                        prev_token = token_type
                        print(
                            f"Value: {token_value}, Type: {token_type}, Length: {len(token_value)}, Line: {current_line}, Pointer: {current_pos}")
                        #tokens.append((token_type, token_value, current_line, current_pos))
                        # print('match: ', token_type, token_value, current_line, current_pos, )

                current_token_len = len(token_value)

                if token_type == 'NEWLINE':
                    current_line += 1
                break
        if not match:

            error_token = input_text[current_pos]
            error_pos = current_pos
            while error_token != ' ' and error_token != '\n' and error_token != '\t' and error_pos < len(input_text) - 1:
                error_pos += 1
                error_token = input_text[error_pos]
            current_token_len = 0
            print(token_type, token_value, current_line, current_pos, 'EROARE ')
        current_pos += current_token_len
        current_token_len = 0
    return tokens

tok = scan("example.txt")