import streamlit as st
import requests
import json
import PyPDF2

# Cargar la API key desde los secretos de Streamlit
api_key = st.secrets["together"]["api_key"]

# Función para extraer texto del PDF
def extraer_texto_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    texto = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        texto += page.extract_text()
    return texto

# Función para obtener el resumen del libro
def obtener_resumen(contenido_libro):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Mensaje para el modelo, donde indicamos que queremos un resumen del contenido
    data = {
        "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "messages": [{"role": "system", "content": "Resume el siguiente libro de más de 100 páginas:"},
                     {"role": "user", "content": contenido_libro}],
        "max_tokens": 2512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1.0,
        "stop": ["<|eot_id|>"],
        "stream": False
    }

    # Hacemos la solicitud a la API de Together
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Interfaz de usuario en Streamlit
st.title("App de Resumen de Libros (PDF)")
st.write("Esta aplicación resume libros de más de 100 páginas utilizando la API de Together.")

# Input para subir un archivo PDF
pdf_file = st.file_uploader("Sube un archivo PDF", type=["pdf"])

# Botón para generar el resumen
if pdf_file is not None:
    # Extraemos el texto del PDF
    with st.spinner("Extrayendo texto del PDF..."):
        texto_pdf = extraer_texto_pdf(pdf_file)

    # Mostrar un fragmento del texto extraído
    st.subheader("Contenido del PDF extraído:")
    st.write(texto_pdf[:2000])  # Mostrar los primeros 2000 caracteres del contenido

    # Botón para generar el resumen
    if st.button("Generar Resumen"):
        with st.spinner("Generando resumen..."):
            resumen = obtener_resumen(texto_pdf)
            if resumen:
                st.subheader("Resumen del Libro:")
                st.write(resumen)
else:
    st.warning("Por favor, sube un archivo PDF para continuar.")
