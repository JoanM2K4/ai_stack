FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema para audio local (micrófono/parlantes) + soporte común
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    portaudio19-dev \
    libasound2-dev \
    pulseaudio \
    ffmpeg \
  && rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Si NO está en requirements.txt, deja esto; si ya está, puedes borrarlo
RUN pip install --no-cache-dir python-dotenv

# Copia tu código
COPY . .

# Ejecuta tu agente como tú lo haces localmente
CMD ["python", "agent.py","start"]
