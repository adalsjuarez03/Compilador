import ply.lex as lex

# Definición de los tokens
tokens = (
    'PROGRAM', 'ID', 'READ', 'PRINTF', 'END',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'COMMA', 
    'PLUS', 'ASSIGN', 'INT', 'STRING', 'NUMERO'  
)

# Diccionario de palabras reservadas
reserved = {
    'programa': 'PROGRAM',
    'read': 'READ',
    'printf': 'PRINTF',
    'end': 'END',
    'int': 'INT'
}

# Reglas para los tokens
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    if t.value in ['a', 'b', 'c']:
        t.description = 'Variable'
        t.category = 'Variable'
    elif t.type == 'ID':
        t.description = 'Identificador'
        t.category = 'ID'
    else:
        t.description = 'Palabra Reservada'
        t.category = 'PR'
    return t

def t_NUMERO(t):
    r'\d+'
    t.description = 'Número'
    t.category = 'Número'
    return t

def t_STRING(t):
    r'\".*?\"'
    t.type = 'STRING'
    t.description = 'Cadena de caracteres'
    t.category = 'Cadena'
    return t

def t_LPAREN(t):
    r'\('
    t.description = 'Paréntesis de apertura'
    t.category = 'Símbolo'
    return t

def t_RPAREN(t):
    r'\)'
    t.description = 'Paréntesis de cierre'
    t.category = 'Símbolo'
    return t

def t_LBRACE(t):
    r'\{'
    t.description = 'Llave de apertura'
    t.category = 'Símbolo'
    return t

def t_RBRACE(t):
    r'\}'
    t.description = 'Llave de cierre'
    t.category = 'Símbolo'
    return t

def t_SEMICOLON(t):
    r';'
    t.description = 'Punto y coma'
    t.category = 'Símbolo'
    return t

def t_COMMA(t):
    r','
    t.description = 'Coma'
    t.category = 'Símbolo'
    return t

def t_PLUS(t):
    r'\+'
    t.description = 'Operador suma'
    t.category = 'Símbolo'
    return t

def t_ASSIGN(t):
    r'='
    t.description = 'Operador asignación'
    t.category = 'Símbolo'
    return t

def t_INT(t):
    r'\bint\b'
    t.type = 'INT'
    t.description = 'Palabra Reservada'
    t.category = 'PR'
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

def tokenize(text):
    lexer.input(text)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        token_info = {
            'line': tok.lineno,
            'token': tok.value,
            'category': tok.category,
            'description': tok.description
        }
        tokens.append(token_info)
    return tokens
