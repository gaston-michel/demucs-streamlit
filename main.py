import streamlit as st
import demucs.separate
import os
import tempfile

# Título del programa
st.title("Separador de Batería")

# Instrucciones
st.write("Sube un archivo de audio para extraer la pista de batería usando Demucs.")

# Subida del archivo
uploaded_file = st.file_uploader("Sube tu archivo de audio", type=["mp3", "wav", "flac", "ogg", "m4a"])

if uploaded_file is not None:
    # Guardar archivo temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        audio_path = temp_file.name

    # Procesar el archivo para separar la batería
    with st.spinner('Procesando el archivo para separar la batería...'):
        demucs.separate.main(["--two-stems", "drums", "-n", "htdemucs", audio_path])
    
    # Obtener el nombre del archivo de salida
    output_dir = os.path.join("separated", "htdemucs", os.path.splitext(os.path.basename(audio_path))[0])
    drums_path = os.path.join(output_dir, "drums.wav")

    # Verificar si la pista de batería fue generada
    if os.path.exists(drums_path):
        st.success("¡Separación completada!")
        
        # Descargar la pista de batería
        with open(drums_path, "rb") as file:
            st.download_button(
                label="Descargar la pista de batería",
                data=file,
                file_name="bateria_separada.wav",
                mime="audio/wav"
            )
    else:
        st.error("No se pudo generar la pista de batería. Revisa el archivo de entrada.")

    # Limpiar archivos temporales
    os.remove(audio_path)
else:
    st.write("Sube un archivo de audio para comenzar.")

