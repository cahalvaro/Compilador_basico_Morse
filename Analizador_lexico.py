import re

class Simbolo:
    def __init__(self, lexema, token):
        self.lexema = lexema 
        self.token = token

    def __repr__(self):
        return "Simbolo"f'("{self.lexema}", "{self.token}")'

class Lexer:
    def __init__(self, codigo):
        self.codigo = codigo
        self.patron = self._compilar_patron() 

    def _compilar_patron(self):
        # Expresiones regulares
        TOKENS = [
            ("NUMERO", r"((-----|\.----|\.\.---|\.\.\.--|\.\.\.\.-|\.\.\.\.\.|-\.\.\.\.|--\.\.\.|---\.\.|----\.)\s)+"), #Digitos
            ("OPERADOR", r"(\.-\.-\.|-\.\.\.\.-|-\.\.-|-\.\.-\.)\s"), #Operadores aritmeticos  
            ("COMPARADOR", r"(\.\.-\.-|\.-\.-\.|-\.\.\.-\s-\.\.\.-)\s"),  # Comparadores
            ("WHITESPACE", r"\s+"),                          # Espacios en blanco (ignorados)
            ("DELIMITADOR", r"(-\.--\.|-\.--\.-)\s"),        # Delimitadores
            ("ASIGNACION", r"(_\.\.\._)\s"),                 #igual
        ]
        # Combina las reglas en un único patrón
        patrones = [f"(?P<{nombre}>{regex})" for nombre, regex in TOKENS]
        return re.compile("|".join(patrones))  # Une todas las reglas con OR (`|`)

    def analizar(self):
        tabla_simbolos = []
        posicion_actual = 0  # Posición inicial del análisis
        linea_actual = 1     # Línea actual del análisis

        while posicion_actual < len(self.codigo):
            match = self.patron.match(self.codigo, posicion_actual)
            if match:
                tipo = match.lastgroup  
                valor = match.group(tipo)
                if tipo == "WHITESPACE" or tipo == "COMMENT":
                    # Actualiza la línea si hay saltos de línea en espacios o comentarios
                    linea_actual += valor.count('\n')
                    posicion_actual = match.end()
                    continue  # Ignora espacios

                # Agrega el token como un símbolo a la tabla
                tabla_simbolos.append(Simbolo(valor, tipo))
                posicion_actual = match.end()  # Avanza la posición actual
            else:
                # Error: el código no coincide con ningún patrón
                fin_linea = self.codigo.find('\n', posicion_actual)
                if fin_linea == -1:
                    fin_linea = len(self.codigo)
                codigo_erroneo = self.codigo[posicion_actual:fin_linea]
                print(f"Error en la línea {linea_actual}: '{codigo_erroneo.strip()}'")
                break 
        return tabla_simbolos

if __name__ == "__main__":
    codigo = """
    -.... ..-.- ----.
    """
    #((125+587)*15)/5
    lexer = Lexer(codigo)
    tabla_simbolos = lexer.analizar()

    # Imprime la tabla de símbolos generada
    print("Tabla de símbolos:")
    print("[")
    for simbolo in tabla_simbolos:
        print(f"    {simbolo},")
    print("]")