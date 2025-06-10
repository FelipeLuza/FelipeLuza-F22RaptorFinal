import pyttsx3
import speech_recognition as sr

def falar_frase_inicial(nome):
    engine = pyttsx3.init()
    engine.setProperty("rate", 160)
    frase = f"{nome}, você é o último piloto. Inimigo à vista. Prepare-se para sobreviver."
    engine.say(frase)
    engine.runAndWait()

def mensagem_inicio():
    print("Jogo iniciado com sucesso!")


def ouvir_comando():
    reconhecedor = sr.Recognizer()
    try:
        with sr.Microphone() as fonte:
            print("Ajustando ruído ambiente...")
            reconhecedor.adjust_for_ambient_noise(fonte, duration=1)
            print("Diga 'jogar' para começar...")
            audio = reconhecedor.listen(fonte, timeout=5)
            print("Áudio capturado, processando...")

        # Salvar o áudio para depuração
        with open("teste_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())
            print("Áudio salvo como teste_audio.wav")

        texto = reconhecedor.recognize_google(audio, language='pt-BR')
        print("Você disse:", texto)

        if "jogar" in texto.lower():
            print("Comando reconhecido: jogar")
            return True
        else:
            print("Comando de voz não reconhecido.")
            return False

    except sr.UnknownValueError:
        print("Não entendi o que foi dito.")
    except sr.RequestError as e:
        print(f"Erro ao acessar o serviço de reconhecimento: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return False

