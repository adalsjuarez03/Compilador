from flask import Flask, render_template, request
from lexer import tokenize  # Asegúrate de tener la función tokenize
from parser import parse_code

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    text = ""
    tokens = []
    error_messages = []
    
    # Variables para los totales
    total_tokens = 0
    total_pr = 0
    total_id = 0
    total_symbols = 0
    total_variables = 0   # Nueva variable total para variables
    total_numeros = 0     # Nueva variable total para números
    total_cadenas = 0     # Nueva variable total para cadenas

    if request.method == 'POST':
        text = request.form['text']
        lines = text.splitlines()

        # Tokenizar cada línea y asignar el número de línea correspondiente
        for line_number, line in enumerate(lines, start=1):
            line_tokens = tokenize(line)  # Tokenizar la línea actual
            for token in line_tokens:
                token['line'] = line_number  # Asignar el número de línea a cada token
                tokens.append(token)  # Agregar tokens a la lista total
                
                # Contar los totales
                total_tokens += 1
                if token['category'] == 'PR':
                    total_pr += 1
                elif token['category'] == 'ID':
                    total_id += 1
                elif token['category'] == 'Variable':  # Contar las variables
                    total_variables += 1
                elif token['category'] == 'Número':    # Contar los números
                    total_numeros += 1
                elif token['category'] == 'Cadena':    # Contar las cadenas
                    total_cadenas += 1
                elif token['category'] == 'Símbolo':
                    total_symbols += 1

        # Realizar el análisis sintáctico y capturar mensajes de error
        error_messages = parse_code(text)

    return render_template('index.html', text=text, tokens=tokens, error_messages=error_messages,
                           total_tokens=total_tokens, total_pr=total_pr, total_id=total_id, 
                           total_symbols=total_symbols, total_variables=total_variables,
                           total_numeros=total_numeros, total_cadenas=total_cadenas)  # Pasar nuevos totales

if __name__ == '__main__':
    app.run(debug=True)