import ply.lex as lex

# The LexToken object arguments:
# 1 - type of the token (provided by the tokens list)
# 2 - value of the token (lexeme)
# 3 - lineno (which is the current line number)
# 4 - lexpos (position of the token relative to the beginning of the input text)

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
    "div": "DIV",
    "integer": "TYPE",
    "boolean": "TYPE"
}

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

    # Note: You should avoid writing individual rules for reserved words
    # so these rules will be triggered for identifiers that include those words as a prefix, like "forget"
    # t_FOR = r'for' 

    # A regular expression rule with some action code 
    # in this case the argument 't' is always an instance of LexToken

    # Number rule
    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Token TYPE rule (different approach than the one used in reserved words)
    #   def t_TYPE(t):
    #       r'integer|boolean'
    #       return t

    # Identifiers rule
    def t_ID(t):
        r'[a-zA-Z][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value,'ID')
        return t

    # Rule to track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(t):
        print("Illegal character:", t.value[0])
        ch = t.value[0]
        lineno = t.lexer.lineno # linha do erro
        pos = t.lexer.lexpos  # posição absoluta do erro
        # armazena uma tupla com informações do erro
        t.lexer.errors.append((lineno, ch, pos))
        t.lexer.skip(1)
  
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
        print(tok)
    
    if lexer.errors:
        print(f"\n{len(lexer.errors)} erro(s) léxico(s) encontrado(s):")
        for lineno, ch, pos in lexer.errors:
            #col = find_column(data, pos)
            print(f"Erro na linha {lineno}: caractere inválido {repr(ch)}")
    else:
        print("\nNenhum erro léxico encontrado.")

if __name__ == '__main__':
    main()
