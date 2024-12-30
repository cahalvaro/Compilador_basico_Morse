class Simbolo:
    def __init__(self, lexema, token):
        self.lexema = lexema
        self.token = token

def verificar_expresion(tabla_simbolos):
    index = 0
    if not tabla_simbolos:
        print("Error: La tabla de símbolos está vacía.")
        return False

    # Detectar si es una comparación o una operación
    if es_comparacion(tabla_simbolos):
        index = comparacion(tabla_simbolos, index)
    else:
        index = operacion(tabla_simbolos, index)

    return index == len(tabla_simbolos)

def es_comparacion(tabla_simbolos):
    # Detectar si la tabla es una comparación
    tiene_comparador = any(simbolo.token == "COMPARADOR" for simbolo in tabla_simbolos)
    return tiene_comparador

def comparacion(tabla_simbolos, index):
    if index >= len(tabla_simbolos) or tabla_simbolos[index].token != "NUMERO":
        print(f"Error: Se esperaba un número en la posición {index}")
        return -1
    index += 1

    if index >= len(tabla_simbolos) or tabla_simbolos[index].token != "COMPARADOR":
        print(f"Error: Se esperaba un comparador en la posición {index}")
        return -1
    index += 1

    if index >= len(tabla_simbolos) or tabla_simbolos[index].token != "NUMERO":
        print(f"Error: Se esperaba un número en la posición {index}")
        return -1

    return index + 1

def operacion(tabla_simbolos, index):
    index = factor(tabla_simbolos, index)
    if index == -1:
        return -1

    while index < len(tabla_simbolos) and tabla_simbolos[index].token == "OPERADOR":
        index += 1
        index = factor(tabla_simbolos, index)
        if index == -1:
            return -1

    return index

def factor(tabla_simbolos, index):
    if index >= len(tabla_simbolos):
        print(f"Error: Se esperaba un factor en la posición {index}")
        return -1

    # Verificar apertura de paréntesis
    if tabla_simbolos[index].token == "DELIMITADOR" and tabla_simbolos[index].lexema == "-.--. ":
        index += 1
        index = operacion(tabla_simbolos, index)
        if index == -1:
            return -1

        if index >= len(tabla_simbolos) or tabla_simbolos[index].lexema != "-.--.- ":
            print(f"Error: Se esperaba '-.--.- ' en la posición {index}")
            return -1

        return index + 1

    # Verificar número
    if tabla_simbolos[index].token == "NUMERO":
        return index + 1

    print(f"Error: Se esperaba un número o una subexpresión en la posición {index}")
    return -1

if __name__ == "__main__":
    tabla_simbolos = [
        Simbolo("-.--. ", "DELIMITADOR"),
        Simbolo("....- ", "NUMERO"),
        Simbolo("-..- ", "OPERADOR"),
        Simbolo("...-- ", "NUMERO"),
        Simbolo("-.--.- ", "DELIMITADOR"),
        Simbolo("-....- ", "OPERADOR"),
        Simbolo("..---", "NUMERO")
    ]
    print("Analizando tabla de símbolos:")
    resultado = verificar_expresion(tabla_simbolos)
    if resultado:
        print("No existen errores sintácticos.")
    else:
        print("Se encontraron errores sintácticos.")


