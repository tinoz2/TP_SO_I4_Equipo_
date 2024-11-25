from funciones import *
path = "juego_consola/prueba_pokemones.csv"

jugar = True
while jugar == True:
    iniciar_juego(path)
    opcion = input("¿Quiere seguir jugando? ")
    if opcion.lower() == "no":
        jugar = False
        print("Cerrando programa...")