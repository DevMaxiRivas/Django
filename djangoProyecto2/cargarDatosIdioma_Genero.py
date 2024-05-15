from catalogo.models import Idioma, Genero

i1 = Idioma(nombre="Español")
i1.save()
i2 = Idioma(nombre="Íngles")
i2.save()
i3 = Idioma(nombre="Portugues")
i3.save()

g1 = Genero(nombre="Ciencia Ficción")
g1.save()
g2 = Genero(nombre="Terror y misterio")
g2.save()
g3 = Genero(nombre="Humor")
g3.save()
