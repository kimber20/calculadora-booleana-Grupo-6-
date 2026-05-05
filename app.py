import streamlit as st
from truth_table import generar_tabla, generar_pdf

st.set_page_config(page_title="Calculadora Lógica", layout="centered")

# Estilo visual blindado contra temas oscuros/claros[cite: 2]
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    div.stButton > button {
        background-color: #FDFDFD !important;
        color: #000000 !important;
        border: 1px solid #CCCCCC !important;
        height: 60px !important;
        font-weight: bold !important;
    }
    .main-btn > div > button {
        background-color: #E2B4BD !important;
        border: 1px solid #D8A3AE !important;
    }
    .download-btn > div > button {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
    }
    .panel {
        background-color: #F8F9FA;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #E9ECEF;
    }
    .display-box {
        background-color: #FFFFFF;
        border: 1px solid #CCCCCC;
        border-radius: 12px;
        padding: 18px 16px;
        min-height: 54px;
        margin-bottom: 18px;
        font-size: 18px;
        color: #111827;
        word-break: break-word;
    }
    </style>
""", unsafe_allow_html=True)

if 'expresion' not in st.session_state:
    st.session_state.expresion = ""

def add(simbolo):
    # Agrega espacio alrededor de cualquier símbolo para evitar concatenaciones
    st.session_state.expresion += f" {simbolo.strip()} "
    
    # Limpiamos espacios dobles accidentales
    st.session_state.expresion = " ".join(st.session_state.expresion.split())

def backspace():
    # Elimina el último bloque o carácter
    st.session_state.expresion = st.session_state.expresion[:-1].rstrip()

def clear():
    st.session_state.expresion = ""

st.markdown('<h2 style="text-align:center; color: #1A1A1A;">LOGIC CALCULATOR</h2>', unsafe_allow_html=True)

# Pantalla de la calculadora corregida[cite: 2]
st.markdown(f'<div class="display-box">{st.session_state.expresion or "&nbsp;"}</div>', unsafe_allow_html=True)

st.markdown('<div class="panel">', unsafe_allow_html=True)
rows = [
    [("¬ NOT", "NOT"), ("∧ AND", "AND"), ("∨ OR", "OR"), ("⊕ XOR", "XOR")],
    [("→ IMP", "->"), ("↔ IFF", "<->"), ("(", "("), (")", ")")],
    [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
    [("⌫", "backspace"), ("CLR", "clear"), ("", ""), ("", "")]
]

for row in rows:
    cols = st.columns(4)
    for i, (label, val) in enumerate(row):
        if not label:
            continue
        if val == "backspace":
            cols[i].button(label, on_click=backspace, key=f"btn_{label}")
        elif val == "clear":
            cols[i].button(label, on_click=clear, key=f"btn_{label}")
        else:
            cols[i].button(label, on_click=add, args=(val,), key=f"btn_{val}")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="main-btn">', unsafe_allow_html=True)
if st.button("CALCULAR TABLA DE VERDAD", use_container_width=True):
    if st.session_state.expresion:
        try:
            vars_list, df_resultado = generar_tabla(st.session_state.expresion)
            if "Error" in df_resultado["Resultado"].tolist():
                st.error("La expresión lógica es inválida. Verifica que uses operadores válidos (AND, OR, NOT, etc.) y variables (A-D), y evita secuencias como variables consecutivas sin operadores.")
            else:
                st.write("---")
                st.dataframe(df_resultado, use_container_width=True)

                # Única opción de PDF corregida[cite: 1]
                pdf_file = generar_pdf(st.session_state.expresion, vars_list, df_resultado)
                st.markdown('<div class="download-btn">', unsafe_allow_html=True)
                st.download_button(
                    label="📄 DESCARGAR REPORTE (PDF)",
                    data=pdf_file,
                    file_name="reporte_logica.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error en la expresión: {e}")
st.markdown('</div>', unsafe_allow_html=True)