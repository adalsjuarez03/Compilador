import ply.yacc as yacc
from lexer import tokens, tokenize  # Importar los tokens y la función de tokenización

# Variable global para almacenar el mensaje de error
syntax_error_message = []

# Estructura de los tokens esperados
estructura_correcta_tokens = [
    "programa", "suma", "(", ")", "{", 
    "int", "a", ",", "b", ",", "c", ";", 
    "read", "a", ";", 
    "read", "b", ";", 
    "c", "=", "a", "+", "b", ";", 
    "printf", "(", '"la suma es"', ")", 
    "end", ";", 
    "}"
]

# Definir las reglas gramaticales
def p_program(p):
    '''program : PROGRAM ID LPAREN RPAREN LBRACE statements RBRACE'''
    p[0] = ('program', p[2], p[6])  # Guardar la información del programa

def p_statements(p):
    '''statements : statement
                  | statement statements'''
    if len(p) == 2:
        p[0] = [p[1]]  # Una declaración simple
    else:
        p[0] = [p[1]] + p[2]  # Varias declaraciones

def p_statement(p):
    '''statement : declaration
                 | read_statement
                 | assign_statement
                 | printf_statement
                 | end_statement'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : INT ID var_list SEMICOLON'''
    p[0] = ('declaration', [p[2]] + p[3])  # Guardar las variables declaradas

def p_var_list(p):
    '''var_list : COMMA ID var_list
                | empty'''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_read_statement(p):
    '''read_statement : READ ID SEMICOLON'''
    p[0] = ('read', p[2])  # Guardar la variable leída

def p_assign_statement(p):
    '''assign_statement : ID ASSIGN ID PLUS ID SEMICOLON'''
    p[0] = ('assign', p[1], p[3], p[5])  # Guardar la asignación

def p_printf_statement(p):
    '''printf_statement : PRINTF LPAREN STRING RPAREN'''
    p[0] = ('printf', p[3])  # Guardar la cadena a imprimir

# Cambiado para tratar 'end' como una palabra reservada
def p_end_statement(p):
    '''end_statement : END SEMICOLON'''
    p[0] = ('end', p[1])  # Guardar el token 'end'

def p_empty(p):
    '''empty :'''
    p[0] = None

# Manejo de errores para sintaxis incorrecta
def p_error(p):
    global syntax_error_message
    if p:
        syntax_error_message.append(f"Error de sintaxis en el token '{p.type}' en la línea {p.lineno}.")
    else:
        syntax_error_message.append("Error de sintaxis: falta 'end'.")

def parse_code(code):
    global syntax_error_message
    syntax_error_message = []  # Reiniciar el mensaje de error antes de cada análisis

    # Tokenizar el código ingresado
    tokens = tokenize(code)  # Usar la función de tokenización del lexer

    # Verificación de estructura
    for i, expected_token in enumerate(estructura_correcta_tokens):
        if i < len(tokens):
            if tokens[i]['token'] != expected_token:
                syntax_error_message.append(f"Error de sintaxis en el token {i + 1}: Se esperaba '{expected_token}'")
                break  # Detener el análisis en el primer error encontrado
        else:
            syntax_error_message.append(f"Error: Faltando token en la posición {i + 1}: Se esperaba '{expected_token}'")
            break  # Detener el análisis en el primer error encontrado

    # Si no hay errores en la verificación de estructura, pasar al análisis sintáctico
    if not syntax_error_message:
        parser.parse(code)  # Analizar el código con PLY

    # Verificar si no hay errores de sintaxis
    if not syntax_error_message:
        syntax_error_message.append("Sintaxis correcta.")  # Mensaje de éxito
        
    return syntax_error_message  # Retornar el mensaje de error, si existe

# Construir el parser
parser = yacc.yacc()
