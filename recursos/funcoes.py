import os, time, speech_recognition, pyttsx3

def limparTela():
    os.system("cls")

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

def pc_falar():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Velocidade da fala
    engine.setProperty('volume', 1)  # Volume (0.0 a 1.0)
    
    engine.say("")
    engine.runAndWait()
    
