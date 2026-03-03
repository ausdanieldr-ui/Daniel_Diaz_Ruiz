import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia
import requests

# visualizar opciones descargadas de idioma de voz
engine = pyttsx3.init()
voces = engine.getProperty('voices')

for voz in voces:
    if 'spanish' in voz.name.lower() or 'es-' in voz.id.lower():
        engine.setProperty('voice', voz.id)
        break

engine.setProperty('rate', 160)  # Velocidad ligeramente más natural


def hablar(mensaje):
    """Pronuncia el mensaje y espera a que termine antes de seguir"""
    print(f"Asistente dice: {mensaje}")  # Para depurar en terminal
    engine.say(mensaje)
    engine.runAndWait()


def transformar_audio_en_texto():

    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera (a veces corrige errores en la escucha)
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
            print("ups, no hay servicio")

            # devolver error
            return "Sigo esperando"


# funcion saludo incial
def saludo_inicial():
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buenos días'
    else:
        momento = 'Buenas tardes'
    hablar(
        f'{momento} soy tu asistente personal. Por favor, dime en que puedo ayudarle')

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buenos días'
    else:
        momento = 'Buenas tardes'

# informar el día de la semana


def pedir_dia():
    fecha = datetime.date.today()
    dias_semana = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves',
                   4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
    meses = {1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio',
             7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'}

    dia_nombre = dias_semana[fecha.weekday()]
    mes_nombre = meses[fecha.month]

    hablar(f'Hoy es {dia_nombre}, {fecha.day} de {mes_nombre} de {fecha.year}')


# informar que hora es
def pedir_hora():
    ahora = datetime.datetime.now()
    hablar(
        f'En este momento son las {ahora.hour} horas con {ahora.minute} minutos y {ahora.second} segundos')


def consultar_noticias_ia():
    # Configuración de la API
    api_key = 'e95d013336304d46a341a5eeb4a22200'
    url = f'https://newsapi.org/v2/top-headlines?category=technology&language=es&apiKey={api_key}'

    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        articulos = datos.get('articles', [])[:3]

        if articulos:
            hablar("Estas son las noticias tecnológicas de hoy:")
            for art in articulos:
                hablar(art['title'])
        else:
            hablar("No he encontrado noticias nuevas en este momento.")
    except:
        hablar("No pude conectar con el servidor de noticias.")

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
            hablar('ahora mismo lo abro')
            webbrowser.open(
                'https://www.google.com/?zx=1756456138580&no_sw_cr=1')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en internet' in pedido:
            hablar('Ya mismo estoy en ello')
            termino = pedido.replace('busca en internet', '').strip()
            hablar(f"Estos son los resultados para {termino}")
            pywhatkit.search(termino)
            continue
        elif 'busca en wikipedia' in pedido:
            # Quitamos la frase de activación y limpiamos espacios
            termino = pedido.replace('busca en wikipedia', '').strip()

            if not termino:
                hablar("No me has dicho qué quieres que busque.")
            else:
                try:
                    wikipedia.set_lang('es')
                    # sentences=1 para que sea un resumen corto
                    resultado = wikipedia.summary(termino, sentences=1)
                    hablar(f"He encontrado esto: {resultado}")
                except Exception:
                    hablar("Lo siento, no pude encontrar esa información.")
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke(language='es', category='all'))
            continue
        elif 'dime las noticias' in pedido or 'noticias' in pedido:
            consultar_noticias_ia()
            continue
        elif 'adiós' in pedido:
            hablar('Me voy a descansar, cualquier cosa me avisas. ¡Adiós!')
        elif 'gracias' in pedido:
            hablar('De nada, para eso estoy aquí. ¡Hasta luego!')
        break


if __name__ == "__main__":
    pedir_cosas()
