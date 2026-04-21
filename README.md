# calculadora-booleana-Grupo-6-
Calculadora Booleana
## 📖 Guía de Uso

🔗 **Acceder a la aplicación:**  
👉 [Abrir Logic Calculator](https://kqzaxqdrybyudpwxwlrwqt.streamlit.app/)

---

### 🧠 ¿Qué hace la app?
La calculadora booleana permite construir expresiones lógicas y generar automáticamente su tabla de verdad.  
Está desarrollada como una aplicación web interactiva usando Streamlit, lo que permite ejecutarla directamente en el navegador sin instalación. :contentReference[oaicite:0]{index=0}

---

### ▶️ Paso 1: Ingresar una expresión

Puedes escribir directamente o usar el teclado.

Ejemplo:
```
A AND B
```

---

### ⌨️ Paso 2: Usar el teclado

Operadores disponibles:

- NOT → ¬ (negación)
- AND → ∧ (conjunción)
- OR → ∨ (disyunción)
- XOR → ⊕ (exclusiva)
- IMP → → (implicación)
- IFF → ↔ (doble implicación)
- ( ) → paréntesis

Variables disponibles:
```
A, B, C, D
```

---

### 🧩 Paso 3: Construir la expresión

Ejemplos:
```
A AND B
¬A OR B
(A AND B) → C
(A XOR B) ↔ D
```

---

### ⚙️ Paso 4: Calcular la tabla

Presiona el botón:

**CALCULAR TABLA DE VERDAD**

---

### 📊 Paso 5: Ver resultados

La app mostrará una tabla con todas las combinaciones posibles.

Ejemplo:

| A | B | Resultado |
|---|---|----------|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

---

### 💾 Paso 6: Descargar resultados

Haz clic en:

**DESCARGAR RESULTADOS (CSV)**

---

### ⚠️ Recomendaciones

- Usa bien los paréntesis
- No dejes expresiones incompletas
- Escribe operadores correctamente

---

### 🎯 Ejemplo completo

```
(A AND B) → (¬A OR B)
```

La aplicación generará automáticamente su tabla de verdad.
