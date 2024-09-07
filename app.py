import streamlit as st
import requests
import json

# Cargar la API key desde los secretos de Streamlit
api_key = st.secrets["together"]["api_key"]

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
st.title("App de Resumen de Libros")
st.write("Esta aplicación resume libros de más de 100 páginas utilizando la API de Together.")

# Input para que el usuario pegue el contenido del libro
libro_input = st.text_area("Introduce el contenido del libro aquí:")

# Botón para generar el resumen
if st.button("Generar Resumen"):
    if len(libro_input) > 0:
        with st.spinner("Generando resumen..."):
            resumen = obtener_resumen(libro_input)
            if resumen:
                st.subheader("Resumen del Libro:")
                st.write(resumen)
    else:
        st.warning("Por favor, introduce el contenido del libro.")
