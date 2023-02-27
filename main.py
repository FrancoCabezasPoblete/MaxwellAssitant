import pyttsx3
import speech_recognition as sr
import wolframalpha as wa
from pygame import mixer
import os
import random
import pywhatkit as kit
from revChatGPT.V1 import Chatbot
from dotenv import load_dotenv

load_dotenv()

chatbot = Chatbot({
    "email": os.getenv("GPTEMAIL"),
    "password": os.getenv("GPTPASSWORD"),
})

engine = pyttsx3.init()

appId = os.getenv("WOLFRAMID")
wolfram = wa.Client(appId)

def speak(text):
    # TTS
    filename = "Temp"+str(random.randint(1,9999))+".wav"
    engine.save_to_file(text, filename)
    engine.runAndWait()
    # Mixer
    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()
    print(text)
    # make a function to chek if the music is playing, if it is, check for voice commands to stop the music or wait until finished

    while mixer.music.get_busy():
        query = parseCommandStop().lower().split()
        if query[0] == 'callate' or query[0] == 'para' or query[0] == 'stop':
            print("Parando...")
            mixer.music.stop()
            break

    mixer.quit()
    os.remove(filename)

def parseCommandStop():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        listener.operation_timeout = 0.8
        listener.phrase_threshold = 1
        listener.pause_threshold = 0.5
        listener.operation_timeout = 1.3
        input_speech = listener.listen(source)

    try:
        print("Recognizing...")
        query = listener.recognize_google(input_speech, language='es-CL')
        print('You said: ' + query)
        return query
    
    except Exception as e:
        print("Say that again please...")
        print('exception: ' + str(e))
        return "None"

def parseCommand():
    listener = sr.Recognizer()
    print("Listening...")
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        listener.pause_threshold = 1.5
        input_speech = listener.listen(source)

    try:
        print("Recognizing...")
        query = listener.recognize_google(input_speech, language='es-CL')
        print('You said: ' + query)
        return query
    
    except Exception as e:
        print("Say that again please...")
        print('exception: ' + str(e))
        return "None"
    

def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def searchWolfram(query = ''):
    res = wolfram.query(query)
    if res['@success'] == False:
        return "No se encontró respuesta"
    else:
        result = ''
        # Question
        pod0 = res['pod'][0]
        pod1 = res['pod'][1]
        # Containt the answer with the highest confidence value
        if ('result' in pod1['@title'].lower()) or ('input' in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            result = listOrDict(pod1['subpod'])
            return result.split('(')[0]
        else:
            question = listOrDict(pod0['subpod'])
            return question.split('(')[0]


if __name__ == "__main__":
    speak("Hola, soy Maxwell y estoy aquí para ayudarte")

    while True:
        query = parseCommand().lower().split()

        if query[0] == 'maxwell' or query[0] == 'max':
            query.pop(0)
            if query[0] == 'di':
                if 'hola' in query:
                    speak("Hola, ¿cómo estás?")
                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)

            # WolframAlpha
            if query[0] == 'cuanto' or query[0] == 'cuánto':
                query = ' '.join(query[2:])
                speak("Calculando...")
                try:
                    speak(searchWolfram(query))
                except Exception:
                    speak("No se pudo calcular")
            if query[0] == 'calcula' or query[0] == 'calculate':
                query = ' '.join(query[1:])
                speak("Calculando...")
                try:
                    speak(searchWolfram(query))
                except Exception:
                    speak("No se pudo calcular")

            # GPT
            if query[0] == "gpt":
                query = ' '.join(query[1:])
                response = ""

                for data in chatbot.ask(query):
                    response = data["message"]
                speak(response)

            if query[0] == 'reproduce':
                query = ' '.join(query[1:])
                speak("Reproduciendo...")
                kit.playonyt(query)

            # Exit                    
            if query[0] == 'apagado' or query[0] == 'apagate':
                speak('Adios!')
                break


