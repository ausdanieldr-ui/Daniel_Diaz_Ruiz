# html--> estructura y contenido, trae la información
# css --> diseño y estilo, le pone la forma
# javascript --> elementos interactivos

import bs4
import requests


resultado = requests.get('https://www.udemy.com/personal/home/')

print(resultado.text)


sopa = bs4.BeautifulSoup(resultado.text, 'lxml')

print(sopa.select('title')[0].getText())

parrafo_especial = sopa.select('p')[3].getText()
print(parrafo_especial)


columna_lateral = sopa.select('.content p')
print(columna_lateral)

for p in columna_lateral:
    print(p.getText())


resultado = requests.get('https://www.udemy.com/topic/python/')

sopa = bs4.BeautifulSoup(resultado.text, 'lxml')

imagenes = sopa.select('img')[0]['src']
print(imagenes)

imagen_curso_1 = requests.get(imagenes)
print(imagen_curso_1.content)  # esto te da imagen en codigo binario


f = open('mi_imagen.jpg', 'wb')
f.write(imagen_curso_1.content)
f.close()
