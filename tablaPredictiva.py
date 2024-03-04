import re

class TablaPredictive:
    def __init__(self):
        self.stack = []
        self.input = []
        
        self.table = {
            ('S', 'LLAVE_ABIERTA'): ['I', 'A', 'B', 'V'],
            ('A', 'AUTOMATA'): ['AUTOMATA'],
            ('V', 'LLAVE_CERRADA'): ['LLAVE_CERRADA'],
            ('B', 'ALFABETO'): ['AL', 'F'],
            ('AL', 'ALFABETO'): ['G', 'DOSPUNTOS', 'SM', 'RA', 'PUNTOYCOMA'],
            ('G', 'ALFABETO'): ['ALFABETO'],
            ('SM', 'LETRA'): ['LETRA'],
            ('SM', 'DIGITO'): ['DIGITO'],
            ('RA', 'COMA'): ['COMA', 'SM', 'RA'],
            ('RA', 'COMA'): ['COMA','SM'],
            ('RA', 'PUNTOYCOMA'): ['epsilon'],
            ('F', 'ACEPTACION'): ['C', 'DOSPUNTOS', 'N', 'R', 'PUNTOYCOMA'],
            ('C', 'ACEPTACION'): ['ACEPTACION'],
            ('N', 'QU'): ['QU', 'D'],
            ('D', 'DIGITO'): ['DIGITO'],
            ('R', 'COMA'): ['COMA', 'N', 'R'],
            ('R', 'PUNTOYCOMA'): ['epsilon'],
            ('I', 'LLAVE_ABIERTA'): ['LLAVE_ABIERTA'],
        }

    def parse(self, tokens):
        self.tokens = tokens
        self.stack = ['$', 'S']  
        self.cursor = 0
        output = []
        
        
        while self.stack:
            
            print(f"Pila: {self.stack}, token: {self.tokens[self.cursor] if self.cursor < len(self.tokens) else '$'}")
            output.append("Pila: " + str(self.stack[:]))
            top = self.stack[-1]  
            current_token = self.tokens[self.cursor][0] if self.cursor < len(self.tokens) else '$'
            
            if top == current_token:  # Coincidencia con un terminal
                self.stack.pop()  
                self.cursor += 1
            elif (top, current_token) in self.table:
                self.stack.pop()  
                symbols = self.table[(top, current_token)]
                if symbols != ['epsilon']:  
                    for symbol in reversed(symbols):
                        self.stack.append(symbol)
            else:
                print(f"No se encontró entrada en la tabla: {top}, {current_token}")
                raise Exception("Error de sintaxis")
        
        if self.cursor == len(self.tokens):
            raise Exception("Error de sintaxis - La entrada no ha sido  completamente")
        print("Análisis correcto")
        
        return "\n".join(output)


def lexer(input_string):
    tokens = []
    token_specs = [
        ('AUTOMATA', r'\bautomata\b'),
        ('ALFABETO', r'\balfabeto\b'),
        ('ACEPTACION', r'\baceptacion\b'),
        ('QU', r'q'),
        ('LETRA', r'[a-z]'),
        ('DIGITO', r'[0-9]'),
        ('LLAVE_ABIERTA', r'\{'),
        ('LLAVE_CERRADA', r'\}'),
        ('PUNTOYCOMA', r'\;'),
        ('DOSPUNTOS', r'\:'),
        ('COMA', r'\,'),
        ('IGNORAR', r'[ \t\n]+'),
        ('TCH', r'.'),
    ]
    
    token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
    for match in re.finditer(token_regex, input_string):
        type = match.lastgroup
        if type == 'IGNORAR':
            continue
        elif type == 'TCH':
            raise RuntimeError(f'legal caracter: {match.group(0)}')
        else:
            tokens.append((type, match.group(0)))
    return tokens


def parse_input(input_string):
    try:
        tokens = lexer(input_string)
        parser = TablaPredictive()
        estado_pila = parser.parse(tokens) 
        return f"Análisis completado .\n final de la pila: {estado_pila}"
        # return estado_pila
    except Exception as e:
        return str(e)


