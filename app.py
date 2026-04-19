import streamlit as st
import pandas as pd
from truth_table import generar_tabla

# 1. Configuración Visual y Estilos
st.set_page_config(page_title="Calculadora Lógica Binaria", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FDFDFD; }
    .panel {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #F0F0F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .panel-header {
        color: #1A1A1A;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 15px;
        text-align: center;
    }
    div.stButton > button {
        background-color: #FFFFFF;
        color: #1A1A1A;
        border: 1px solid #EAEAEA;
        border-radius: 6px;
        height: 55px !important;
        width: 100%;
        font-size: 14px !important;
        white-space: pre-line;
    }
    .main-action > div > button {
        background-color: #E2B4BD !important; 
        font-weight: 700 !important;
        color: #1A1A1A !important;
    }
    [data-testid="column"] { padding: 0px 3px !important; }
    </style>
""", unsafe_allow_html=True)

if 'expresion' not in st.session_state:
    st.session_state.expresion = ""

def add(simbolo):
    operadores = ["NOT ", "AND ", "OR ", "XOR ", " -> ", " <-> "]
    if simbolo in operadores:
        if st.session_state.expresion.endswith(" ") or st.session_state.expresion == "":
            st.session_state.expresion += simbolo
        else:
            st.session_state.expresion += " " + simbolo
    else:
        st.session_state.expresion += simbolo

def backspace():
    if st.session_state.expresion.endswith(" "):
        st.session_state.expresion = st.session_state.expresion[:-2]
    else:
        st.session_state.expresion = st.session_state.expresion[:-1]

def clear():
    st.session_state.expresion = ""

st.markdown('<h2 style="text-align:center; color:#1A1A1A; font-weight:200;">LOGIC CALCULATOR</h2>', unsafe_allow_html=True)

st.text_input("Display", value=st.session_state.expresion, disabled=True, label_visibility="collapsed")

st.markdown('<div class="panel"><p class="panel-header">Keypad Control</p>', unsafe_allow_html=True)

rows = [
    [("¬\nNOT", "NOT "), ("∧\nAND", "AND "), ("∨\nOR", "OR "), ("⊕\nXOR", "XOR ")],
    [("→\nIMP", " -> "), ("↔\nIFF", " <-> "), ("T\n(1)", "1"), ("⊥\n(0)", "0")],
    [("(", "("), (")", ")"), ("A", "A"), ("B", "B")],
    [("C", "C"), ("D", "D"), ("⌫", "backspace"), ("CLR", "clear")]
]

for row in rows:
    cols = st.columns(4)
    for i, (label, val) in enumerate(row):
        if val == "backspace":
            cols[i].button(label, on_click=backspace, key=f"btn_{label}")
        elif val == "clear":
            cols[i].button(label, on_click=clear, key=f"btn_{label}")
        else:
            cols[i].button(label, on_click=add, args=(val,), key=f"btn_{val}")

st.markdown('</div>', unsafe_allow_html=True)

st.write("##")
st.markdown('<div class="main-action">', unsafe_allow_html=True)
if st.button("CALCULAR TABLA DE VERDAD", use_container_width=True):
    if st.session_state.expresion:
        try:
            vars_list, df_resultado, df_exportar = generar_tabla(st.session_state.expresion)
            
            st.write("---")
            st.dataframe(df_resultado, use_container_width=True)

            # --- SOLUCIÓN PARA EXCEL ---
            # Usamos 'utf-8-sig' para que Excel reconozca el signo → correctamente
            csv = df_exportar.to_csv(index=False, header=False, encoding='utf-8-sig').encode('utf-8-sig')
            
            st.download_button(
                label="📥 DESCARGAR RESULTADOS (CSV)",
                data=csv,
                file_name='tabla_verdad.csv',
                mime='text/csv',
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Error: {e}")