import pandas as pd
import itertools
import re

def extraer_variables(expr):
    return sorted(set(re.findall(r'\b[A-Z]\b', expr)))

def evaluar_expresion(expr, valores):
    expr = expr.upper()
    expr = expr.replace("AND", " and ").replace("OR", " or ").replace("NOT", " not ").replace("XOR", " ^ ")
    expr = re.sub(r'(\w+)\s*->\s*(\w+)', r'(not \1 or \2)', expr)
    expr = re.sub(r'(\w+)\s*<->\s*(\w+)', r'(\1 == \2)', expr)

    for var, val in valores.items():
        expr = re.sub(rf'\b{var}\b', str(bool(val)), expr)

    try:
        return int(eval(expr))
    except:
        raise ValueError("Expresión inválida")

def generar_tabla(expr):
    variables = extraer_variables(expr)
    if not variables:
        raise ValueError("No hay variables válidas")

    combinaciones = list(itertools.product([0, 1], repeat=len(variables)))
    
    # Lista para la previsualización en la App (Formato Tabla)
    data_tabla = []
    # Lista para el formato especial del ejemplo visual (Formato CSV)
    data_visual = []

    for comb in combinaciones:
        valores = dict(zip(variables, comb))
        resultado = evaluar_expresion(expr, valores)
        
        # 1. Guardamos datos para la tabla normal de Streamlit
        data_tabla.append(list(comb) + [resultado])
        
        # 2. Creamos el formato "00 → 0" solicitado
        combinacion_str = "".join(map(str, comb))
        fila_visual = f"{combinacion_str} → {resultado}"
        data_visual.append(fila_visual)

    df_normal = pd.DataFrame(data_tabla, columns=variables + ["Resultado"])
    # Este es el DataFrame que usaremos para el CSV descargable
    df_csv = pd.DataFrame(data_visual, columns=["Tabla de Verdad Binaria"])
    
    return variables, df_normal, df_csv