import os, time, speech_recognition, pyttsx3


def limparTela():
    os.system("cls" if os.name == "nt" else "clear")

def aguarde(segundos):
    time.sleep(segundos)

def reconhecimentoVoz():
    reconhecedor = speech_recognition.Recognizer()
    microfone = speech_recognition.Microphone()

    with microfone as fonte:
        reconhecedor.adjust_for_ambient_noise(fonte)
        print("Aguardando comando de voz...")
        audio = reconhecedor.listen(fonte)

    try:
        comando = reconhecedor.recognize_google(audio, language="pt-BR")
        print(f"Comando reconhecido: {comando}")
        return comando.lower()
    except speech_recognition.UnknownValueError:
        print("Não foi possível reconhecer o comando.")
        return ""
    except speech_recognition.RequestError as e:
        print(f"Erro ao solicitar reconhecimento de voz: {e}")
        return ""

def pc_falar(texto, voz_grossa=False):
    engine = pyttsx3.init()
    engine.setProperty('rate', 140)     # Velocidade da fala
    engine.setProperty('volume', 1.0)   # Volume máximo

    vozes = engine.getProperty('voices')

    # Tenta selecionar uma voz masculina ou "grossa"
    for voz in vozes:
        if voz_grossa and ("brazil" in voz.name.lower() or "male" in voz.name.lower()):
            engine.setProperty('voice', voz.id)
            break
    else:
        # Se não encontrar uma voz específica, usa a padrão
        engine.setProperty('voice', vozes[0].id)

    print(f"Falando: {texto}")
    engine.say(texto)
    engine.runAndWait()