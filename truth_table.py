import pandas as pd
import itertools
import re
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def extraer_variables(expr):
    # Detecta variables A, B, C, D evitando letras dentro de operadores
    temp = re.sub(r'(NOT|AND|OR|XOR|->|<->)', ' ', expr)
    return sorted(list(set(re.findall(r'[A-D]', temp))))

def evaluar_expresion(expr, valores):
    # BLINDAJE: Agregamos espacios alrededor de CUALQUIER símbolo especial
    temp = re.sub(r'([()∧¬∨⊕→↔]|NOT|AND|OR|XOR|->|<->|0|1)', r' \1 ', expr)
    
    # Traducción a sintaxis de Python pura
    op_py = temp.replace("NOT", " not ").replace("AND", " and ").replace("XOR", " != ").replace("OR", " or ")
    op_py = op_py.replace("<->", " == ").replace("->", " <= ")
    op_py = op_py.replace("1", " True ").replace("0", " False ")
    op_py = re.sub(r'\bnot\s*(\([^()]*\]|[A-Za-z0-9_]+)', r'(not \1)', op_py)
    op_py = op_py.strip()
    
    try:
        # Evalúa la expresión de forma aislada para evitar errores de sintaxis[cite: 2]
        resultado = eval(op_py, {"__builtins__": None}, valores)
        return 1 if resultado else 0
    except Exception:
        return "Error"

def generar_tabla(expr):
    variables = extraer_variables(expr)
    combinaciones = list(itertools.product([1, 0], repeat=len(variables)))
    
    filas = []
    for combo in combinaciones:
        valores = dict(zip(variables, [bool(v) for v in combo]))
        res = evaluar_expresion(expr, valores)
        filas.append(list(combo) + [res])
    
    df_resultado = pd.DataFrame(filas, columns=variables + ["Resultado"])
    return variables, df_resultado

def generar_pdf(expr, variables, df_normal):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Reporte de Tabla de Verdad", styles['Title']))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"<b>Expresión:</b> {expr}", styles['Normal']))
    elementos.append(Spacer(1, 24))

    encabezados = variables + ["Resultado"]
    datos_pdf = [encabezados] + df_normal.values.tolist()

    tabla = Table(datos_pdf)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    tabla.setStyle(style)
    
    elementos.append(tabla)
    doc.build(elementos)
    buffer.seek(0)
    return buffer.getvalue()