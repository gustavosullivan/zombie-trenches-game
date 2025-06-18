import sys
from cx_Freeze import setup, Executable
import os

incluir_arquivos = [
    ("recursos/"),  # Inclui toda a pasta 'recursos'
    ('logs', 'logs')  # Se você também usar a pasta de logs, inclua-a
]

build_exe_options = {
    'packages': ['pygame', 'random', 'os', 'math', 'datetime', 'speech_recognition', 'pyttsx3'],
    "includes": [
        "pyttsx3.drivers", 
        "aifc", 
        "chunk", 
        "wave", 
        "pyaudio", 
        "array", 
        "struct", 
        "math", 
        "speech_recognition", 
        "audioop"
    ],
    'include_files': incluir_arquivos,  # Incluir a pasta 'recursos' inteira
}

# Configuração do cx_Freeze para criar o executável
setup(
    name="Defenda o Tesouro",  # Nome do jogo
    version="1.0",  # Versão do jogo
    description="Jogo de defesa de tesouro",  # Descrição do jogo
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=None)],  # Altere para o nome correto do seu arquivo principal
)
