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
for voz in engine.getProperty('voices'):
    print(voz)

# escuchar nuestro microfono y devolver el audio como texto


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


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

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

    mensaje = f'Hoy es {dia_nombre}, {fecha.day} de {mes_nombre} de {fecha.year}'
    print(mensaje)
    hablar(mensaje)


# informar que hora es
def pedir_hora():
    ahora = datetime.datetime.now()
    mensaje = f'En este momento son las {ahora.hour} y {ahora.minute} minutos'
    print(mensaje)
    hablar(mensaje)


def consultar_noticias_ia():
    # Configuración de la API
    api_key = 'e95d013336304d46a341a5eeb4a22200'
    url = f'https://newsapi.org/v2/everything?q=Artificial Intelligence&language=es&sortBy=publishedAt&pageSize=3&apiKey={api_key}'

    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        articulos = datos['articles']

        hablar(
            "He encontrado las 3 noticias más recientes sobre inteligencia artificial:")

        for i, articulo in enumerate(articulos):
            titulo = articulo['title']
            hablar(f"Noticia {i+1}: {titulo}")
            # Para que lo tengas en consola por si quieres leerlo
            print(f"Enlace: {articulo['url']}")

    except:
        hablar("Perdone, he tenido problemas al conectar con el servidor de noticias")

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
        elif 'busca en wikipedia' in pedido:
            hablar('Perfecto, voy a buscarlo')
            termino_busqueda = pedido.replace('busca en wikipedia', '').strip()
            if termino_busqueda == "":
                hablar("No me has dicho qué quieres que busque.")
            else:
                try:
                    wikipedia.set_lang('es')
                    resultado = wikipedia.summary(
                        termino_busqueda, sentences=1)
                    hablar('En wikipedia he encontrado lo siguiente: ')
                    hablar(resultado)
                except:
                    hablar("No he podido encontrar información sobre eso")
            continue
        elif 'busca en internet' in pedido:
            hablar('Voy a ello')
            termino = pedido.replace('busca en internet', '').strip()
            pywhatkit.search(termino)
            hablar(f'Esto es lo que he encontrado sobre {termino}')
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'dime las noticias' in pedido or 'artículos de ia' in pedido:
            consultar_noticias_ia()
            continue
        elif 'adiós' in pedido:
            hablar('Es un placer para mí ayudarle, que tenga buen día')
            break


pedir_cosas()
