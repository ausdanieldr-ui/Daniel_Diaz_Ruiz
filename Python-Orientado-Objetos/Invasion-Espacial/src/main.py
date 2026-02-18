import pygame
import random
import math
import os
from pygame import mixer

# cofigurar la ruta de los archivos
ruta_src = os.path.dirname(os.path.abspath(__file__))
ruta_base = os.path.dirname(ruta_src)
ruta_assets = os.path.join(ruta_base, 'assets')


def obtener_ruta(nombre_archivo):
    return os.path.join(ruta_assets, nombre_archivo)


# Iniciar Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Título e Icono
pygame.display.set_caption("Invasión Dorito", )
icono = pygame.image.load(obtener_ruta("ovni.png"))
pygame.display.set_icon(icono)
fondo = pygame.image.load(obtener_ruta("fondo.png"))


# agregar musica
mixer.music.load(obtener_ruta("MusicaFondo.mp3"))
mixer.music.set_volume(0.6)
mixer.music.play(-1)


# variables del Jugador
img_jugador = pygame.image.load(obtener_ruta("tractores.png"))
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load(obtener_ruta("trump.png")))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(5)
    enemigo_y_cambio.append(50)


# variables de la bala
img_bala = pygame.image.load(obtener_ruta("pajita.png"))
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 5
bala_visible = False


# Puntos
puntos = 0
fuente = pygame.font.Font(obtener_ruta('Begok v15_2015___free.ttf'), 32)
texto_x = 10
texto_y = 10

# texto final del juego
fuente_final = pygame.font.Font(obtener_ruta('begokv15__2015___free.otf'), 40)


def texto_final():
    mi_fuente_final = fuente_final.render(
        "juego terminado", True, (255, 255, 255))
    subtexto = fuente.render(
        "pulsa 'r' para volver a jugar", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (90, 300))
    pantalla.blit(subtexto, (120, 360))


# funcion mostrar puntos
def mostrar_puntos(x, y):
    texto = fuente.render(f'puntos {puntos}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

# función jugador


def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

# función enemigo


def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

# función detectar colisiones


def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2-x_1, 2) + math.pow(y_2-y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# loop del juego
juego_terminado = False
se_ejecuta = True

while se_ejecuta:
    # imagen de fono
    pantalla.blit(fondo, (0, 0))

    # iterar eventos
    for evento in pygame.event.get():

        # Evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -3
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 3
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound(obtener_ruta('disparo.mp3'))
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

            if evento.key == pygame.K_r and juego_terminado:
                puntos = 0
                juego_terminado = False
                for i in range(cantidad_enemigos):
                    enemigo_x[i] = random.randint(0, 736)
                    enemigo_y[i] = random.randint(50, 200)

        # evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # modificar ubicación jugador del jugador
    jugador_x += jugador_x_cambio

    # mantener dentro de los bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # modificar ubicación jugador del enemigo
    for e in range(cantidad_enemigos):
        enemigo_x[e] += enemigo_x_cambio[e]

        # fin del juego
        if enemigo_y[e] > 470:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            juego_terminado = True
            texto_final()
            break

    # mantener dentro de los bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 3
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -3
            enemigo_y[e] += enemigo_y_cambio[e]

        # colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound(obtener_ruta('Golpe.mp3'))
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntos += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x, jugador_y)

    mostrar_puntos(texto_x, texto_y)

    # actualizar
    pygame.display.update()
