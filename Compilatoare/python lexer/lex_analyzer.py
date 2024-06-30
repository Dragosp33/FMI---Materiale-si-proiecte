import re

def lex_analyzer(src_file):
    token_patterns = [
        (r'\b(if|else|elif|while|for|in|def|class|import|from|as|return|break|continue|pass|raise|try|except|' \
         r'finally|with|yield|lambda|global|nonlocal|assert|and|or|not|True|False|None|is)\b', 'KEYWORD'),

        (r'[a-zA-Z_]\w*', 'IDENTIFIER'),

        (r'\d+(\.\d*)?', 'NUMBER'),

        (r'[\+\-\*/%]', 'ARITHMETIC_OP'),

        (r'(==|!=|<=|>=|<|>)', 'COMPARISON_OP'),

        (r'[\&\|\^\~]', 'BITWISE_OP'),

        (r'=', 'ASSIGNMENT'),

        (r'[\(\)]', 'PARENTHESIS'),

        (r'[\[\]]', 'BRACKET'),

        (r'[\{\}]', 'BRACE'),

        (r'[\:\;\.\,\!\?]', 'PUNCTUATOR'),

        (r'\#.*', 'COMMENT'),

        (r'\"\"\"[\s\S]*?\"\"\"', 'MULTI_COMMENT'),

        (r'[\@\$]', 'SPECIAL_CHARACTER'),
    ]

    with open(src_file, 'r') as f:
        file = f.read()

    pointer = 0
    prev_len = 0
    line_no = 1

    while pointer < len(file):
        # Adaugam lungimea Token-ului anterior pointer-ului curent
        pointer = pointer + prev_len

        # Verifica daca caracterul curent este spatiu sau EndLine
        while pointer < len(file) and file[pointer].isspace():
            if file[pointer] == '\n':
                line_no = line_no + 1
            pointer = pointer + 1

        if pointer >= len(file):
            break

        ok = False
        for ptn, t_type in token_patterns:
            # Pattern object pentru verificare
            regex = re.compile(ptn)
            # Verifica daca este match in fisier de la pointerul dat
            match = regex.match(file, pointer)

            if match:
                ok = True
                # Retinem valoarea match-ului gasit (0 - returns the entire match)
                value = match.group(0)
                # Afisam informatiile Token-ului
                print(f"Value: {value}, Type: {t_type}, Length: {len(value)}, Line: {line_no}, Pointer: {pointer}")
                # Retinem lungimea token-ului anterior
                prev_len = len(value)
                break

        # Nu a fost gasit match
        if not ok:
            print(f"Lexical error: Match not found for the Character '{file[pointer]}'")
            pointer = pointer + 1
            # Resetam lunginea Token-ului anterior
            prev_len = 0


if __name__ == '__main__':
    src_file = "example.txt"
    lex_analyzer(src_file)