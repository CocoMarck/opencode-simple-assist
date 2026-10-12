# Changelog
- **LISTO**: Mandarle una ordenes a opencode, con run.
- **LISTO** TTS, espeak obtiene output de opencode, y lo lee.
- **FALTA**: Crear sesión fija al dia.
- **FALTA**: Construcción de prompt con `Speech to Text` usando vosk.
- **FALTA**: Palabra clave al principio de frase, para recibir orden. Ejemplo: `Asistente, abre el navegador web.`
- **FALTA**: Normalizar texto para el TTS. 
    - Debe leer ABC, números, símbolos comunes (@,#,>,<), y de matemáticas .
    - No debe leer palabras con mas de 100 caracteres.
    - Debe entender el estilo markdown. Transcribir lo que sea posible a texto legible, como por ejemplo: "caja de código", para las triple comillas invertidas.