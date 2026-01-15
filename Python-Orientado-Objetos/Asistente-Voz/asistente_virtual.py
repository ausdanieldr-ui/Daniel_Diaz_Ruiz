import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# visualizar opciones descargadas de idioma de voz
engine = pyttsx3.init()
for voz in engine.getProperty('voices'):
    print(voz)

# escuchar nuestro microfono y devolver el audio como texto


def transformar_audio_en_texto():

    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera (a vece corrige errores en la escucha)
        r.pause_threshold = 0.8

        # informar que comenzo la grabacion
        print("Ya puedes hablar")

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language="es-ES")

            # prueba de que puedo ingresar
            print("Dijiste: " + pedido)

            # devolver pedido
            return pedido

        # en caso de que no entienda el audio
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print("ups, no te entendí")

            # devolver error
            return "Sigo esperando"

        # en caso de no resolver el pedido
        except sr.RequestError:

            # prueba de que no comprendio el audio
            print("ups, no hay servivio")

            # devolver error
            return "Sigo esperando"

        # error inesperado
        except:

            # prueba de que no comprendio el audio
            print("ups, algo ha salido mal")

            # devolver error
            return "Sigo esperando"


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # encender el motor de pyttsx3
    engine = pyttsx3.init()

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el día de la semana
def pedir_dia():

    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para el dia de semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionarios semana
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}

    # decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# informar que hora es
def pedir_hora():

    # crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} y {hora.minute}'
    print(hora)

    # decir la hora
    hablar(hora)


# funcion saludo incial
def saludo_inicial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buenos días'
    else:
        momento = 'Buenas tardes'

    # decir el saludo
    hablar(
        f'{momento} soy tu asistente personal. Por favor, dime en que puedo ayudarle')


# funcion centro de pedidos
def pedir_cosas():

    # activar el saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    # loop central
    while comenzar:

        # activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abre youtube' in pedido:
            hablar('Será un placer abrir youtube para usted')
            webbrowser.open('https://www.youtube.com/')
            continue
        elif 'abre el navegador' in pedido:
            hablar('Lo que usted quiera señor')
            webbrowser.open(
                'https://www.google.com/?zx=1756456138580&no_sw_cr=1')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Perfecto, voy a buscarlo')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('En wikipedia he encontrado lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Voy a ello')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'abre spotify' in pedido:
            hablar('Okey, abro spotify')
            webbrowser.open('https://open.spotify.com/')
            continue
        elif 'reproduce' in pedido:
            hablar('Me gusta, voy a ponerlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(
                    f'Las encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar("Perdone, pero no lo he encontrado")
                continue

        elif 'adiós' in pedido:
            hablar('Es un placer para mí ayudarle, que tenga buen día')
            break


pedir_cosas()
