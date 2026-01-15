
# vamos a ver en una web que se llama toscrape, que libros tienen una puntuación de 4 o 5 estrellas

# para explorar varias paginas
import requests
import bs4
for n in range(1, 11):
    print(url_base.format(n))


resultado = requests.get(url_base.format('1'))
sopa = bs4.BeautifulSoup(resultado.text, 'lxml')


libros = sopa.select('.product_pod')

# los espacios vacios deben sustitutirse por: .
ejemplo = libros[0].select('a')[1]['title']
print(ejemplo)


# crear url sin numero de pagina
url_base = 'https://books.toscrape.com/catalogue/page-{}.html'

# lista de titulos con 4 o 5 estrellas
titulos_rating_alto = []

# iterar paginas
for pagina in range(1, 11):

    # crear sopa en cada pagina
    url_pagina = url_base.format(pagina)
    resultado = requests.get(url_pagina)
    sopa = bs4.BeautifulSoup(resultado.text, 'lxml')

    # seleccion datos de los libros
    libros = sopa.select('.product_pod')

    # iterar libros
    for libro in libros:

        # chequear 4 o 5 estrellas
        if len(libro.select('.star-rating.Four')) != 0 or len(libro.select('.star-rating.Five')) != 0:

            # guardar titulo variable
            titulo_libro = libro.select('a')[1]['title']

            # agregar el libro a lista
            titulos_rating_alto.append(titulo_libro)


# ver libros de 4 y 5 estrellas en consola
for t in titulos_rating_alto:
    print(t)
