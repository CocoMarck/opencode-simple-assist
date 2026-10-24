echo APT packages
sudo apt update
sudo apt install -y \
  python3-venv \
  python3-pip \
  portaudio19-dev \
  libportaudio2 \
  pulseaudio-utils \
  alsa-utils \
  unzip \
  wget

echo Crear entorno virtual
python3 -m venv .venv

# Actualizar pip dentro del entorno
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r ./requirements.txt


echo Descargar modelo vosk es
mkdir -p models
cd models

# Descargar modelo pequeño para español
wget https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip

# Descomprimir
unzip vosk-model-small-es-0.42.zip

# Limpiar zip
rm vosk-model-small-es-0.42.zip

# Volver a la raíz
cd ..

