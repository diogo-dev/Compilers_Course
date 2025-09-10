import ply.lex as lex

# The LexToken object arguments:
# 1 - type of the token (provided by the tokens list)
# 2 - value of the token (lexeme)
# 3 - lineno (which is the current line number)
# 4 - lexpos (position of the token relative to the beginning of the input text)

# Important observation about lexer attributes
'''
All internal attributes of the lexer (with the exception of lineno) have names that are prefixed by lex 
(e.g., lexdata,``lexpos``, etc.). Thus, it is perfectly safe to store attributes in the lexer 
that do not have names starting with that prefix or a name that conflicts with one of the predefined methods 
(e.g., input(), token(), etc.).

We've used a internal lexer attribute called 'errors' to store lexical errors found during the analysis.
We initialize it as an empty list when we create the lexer object and we append tuples with information
about the errors found (line number, character and position in the input text).
'''

# Another important observation about token rules for reserved words
'''
Note: You should avoid writing individual rules for reserved words
so these rules will be triggered for identifiers that include those words as a prefix, like "forget"
t_FOR = r'for' 
'''

# Dictionaty of reserved words for RASCAL
reserved = {
    "program": "PROGRAM",
    "var": "VAR",
    "procedure": "PROCEDURE",
    "function": "FUNCTION",
    "begin": "BEGIN",
    "end": "END",
    "false": "FALSE",
    "true": "TRUE",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "while": "WHILE",
    "do": "DO",
    "read": "READ",
    "write": "WRITE",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
    "div": "DIV"
}

# If is necessaty to pass the invalid tokens to the parser, we should add them to the tokens list 
# invalid_tokens = [
#     'INVALID_NUMID'
# ]

# The list token names
tokens = [
    'NUMBER',
    'ID',
    'TYPE',
    'LPAREN',
    'RPAREN',
    'DOT',
    'COMMA',
    'SCOLON',
    'PLUS',
    'MINUS',
    'TIMES',
    'EQUAL',
    'DIFF',
    'GREATER',
    'LOWER',
    'GREATER_E',
    'LOWER_E',
    'ASSIGN',
    'COLON'
] + list(reserved.values()) 

def MyLexer():
    # Regular expression rules for simple tokens
    t_LPAREN    = r'\('
    t_RPAREN    = r'\)'
    t_DOT       = r'\.'
    t_COMMA     = r','
    t_SCOLON    = r';'
    t_PLUS      = r'\+'
    t_MINUS     = r'-'
    t_TIMES     = r'\*'
    t_GREATER_E = r'>='
    t_LOWER_E   = r'<='
    t_DIFF      = r'<>'
    t_GREATER   = r'>'
    t_LOWER     = r'<'
    t_EQUAL     = r'='
    t_ASSIGN    = r':='
    t_COLON     = r':'
    # Ignore white spaces and tabs
    t_ignore = ' \t'

    # Invalid handling rule for numbers followed by letters (e.g., 123abc)
    def t_INVALID_NUMID(t):
        r'\d+[a-zA-Z_]+'
        print(f"Erro léxico: Formação incorreta de identificador '{t.value}'")
        ch = t.value
        lineno = t.lexer.lineno # linha do erro
        pos = t.lexer.lexpos  # posição absoluta do erro
        # armazena uma tupla com informações do erro
        t.lexer.errors.append((lineno, ch, pos))
    
    # Invalid handling rule for floating point numbers (e.g., 12.34 or .56)
    def t_INVALID_FLOAT_NUMBER(t):
        r'\d+\.\d*|\.\d+'
        print(f"Erro léxico: Número em ponto flutuante não permitido '{t.value}'")
        ch = t.value
        lineno = t.lexer.lineno 
        pos = t.lexer.lexpos  
        t.lexer.errors.append((lineno, ch, pos))

    # Number rule
    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Token TYPE rule (different approach than the one used in reserved words)
    def t_TYPE(t):
        r'integer|boolean'
        return t

    # Identifiers rule
    def t_ID(t):
        r'[a-zA-Z][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value,'ID')
        return t

    # Rule to track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule for illegal characters (e.g., @, $, %, ^, &)
    def t_error(t):
        print("Illegal character:", t.value[0])
        ch = t.value[0]
        lineno = t.lexer.lineno 
        pos = t.lexer.lexpos  
        t.lexer.errors.append((lineno, ch, pos))
        t.lexer.skip(1)
  
    # Build the lexer
    lexer = lex.lex()
    lexer.errors = [] 
    
    return lexer

def main():
    lexer = MyLexer()

    # Reading and external file
    with open('./exampleCode.txt', 'r', encoding='utf-8') as file:
        data = file.read()

    # Providing the lexer with the input data
    lexer.input(data)

    print("Tokens:")
    for tok in lexer:
        print(f"({tok.type}, {repr(tok.value)})")
    
    if lexer.errors:
        print(f"\n{len(lexer.errors)} erro(s) léxico(s) encontrado(s):")
        for lineno, ch, pos in lexer.errors:
            #col = find_column(data, pos)
            print(f"Erro na linha {lineno}: caractere inválido {repr(ch)}")
    else:
        print("\nNenhum erro léxico encontrado.")

if __name__ == '__main__':
    main()
