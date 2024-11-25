import random
import re
import json
from datetime import *
from time import *
from os import system
from datetime import datetime
import time

def crear_diccionario_carta(registro:list)->dict:
    
    diccionario_carta = {}

    diccionario_carta["nombre"] = registro[0]
    diccionario_carta["velocidad"] = int(registro[1])
    diccionario_carta["fuerza"] = int(registro[2])
    diccionario_carta["elemento"] = registro[3]
    diccionario_carta["peso"] = float(registro[4])
    diccionario_carta["altura"] = float(registro[5])

    return diccionario_carta


def parsear_csv(path:str)->list:
    with open(path,"r") as archivo_cartas:

        archivo_cartas.readline()

        lista_diccionarios = []
        for linea in archivo_cartas:

            registro = re.split(",|\n",linea)
            diccionario_carta = crear_diccionario_carta(registro)

            lista_diccionarios.append(diccionario_carta)

    return lista_diccionarios

def asignar_valores_elemento(diccionario: dict):
    elemento = diccionario["elemento"]
    
    if elemento == "electricidad":
        valor_elemento = random.randint(20, 40)
    elif elemento == "fuego":
        valor_elemento = random.randint(20, 40)
    elif elemento == "agua":
        valor_elemento = random.randint(20, 40)
    elif elemento == "tierra":
        valor_elemento = random.randint(20, 40)
    elif elemento == "aire":
        valor_elemento = random.randint(20, 40)
    else:
        valor_elemento = random.randint(1, 15)
        
    diccionario["valor_elemento"] = valor_elemento

    return diccionario

def asignar_valores_random_atributos(lista_diccionarios: list) -> list:
    for diccionario in lista_diccionarios:
        diccionario = asignar_valores_elemento(diccionario)
    return print(lista_diccionarios)

def mezclar_baraja(baraja: list)->list:

    for i in range(len(baraja)):
        indice_mezcla = random.randint(0, len(baraja)-1)
        while indice_mezcla == i:
            indice_mezcla = random.randint(0, len(baraja)-1)
        temporal = baraja[i]
        baraja[i] = baraja[indice_mezcla]
        baraja[indice_mezcla] = temporal
    return baraja

def repartir_mazo(mazo:list,mazo_jugador_uno: list,mazo_jugador_dos: list, cantidad_cartas:int)->list:
    estado = False
    if type(mazo) == list:
        for i in range(cantidad_cartas):
            carta_jugador_uno = mazo.pop(0)
            carta_jugador_dos = mazo.pop(0)
            mazo_jugador_uno.append(carta_jugador_uno)
            mazo_jugador_dos.append(carta_jugador_dos)
    return estado


def asignar_nombres()->list:
    nombre = input("Ingrese su nombre: ")
    return nombre

def sortear_atributo(lista: list)->str:
    atributos = list(lista[0].keys())
    atributos.remove("nombre")
    atributo_aleatorio = random.choice(atributos)
    return atributo_aleatorio

def leer_lista(lista: list):
    for i in range(len(lista)):
        print(lista[i])

def comparar_cartas(mazo_jugador_uno: list, mazo_jugador_dos: list, atributo: str)->None|bool:
    
    estado_ronda = None

    carta_jugador_uno = mazo_jugador_uno[0]
    carta_jugador_dos = mazo_jugador_dos[0]

    if carta_jugador_uno[atributo] > carta_jugador_dos[atributo]:
        estado_ronda = True
    elif carta_jugador_uno[atributo] < carta_jugador_dos[atributo]:
        estado_ronda = False
    
    return estado_ronda

def llevar_cartas_mesa(mazo_mesa: list, mazo_jugador_uno: list, mazo_jugador_dos)->list:
    carta_jugador_uno = mazo_jugador_uno.pop(0)
    carta_jugador_dos = mazo_jugador_dos.pop(0)

    mazo_mesa.append(carta_jugador_uno)
    mazo_mesa.append(carta_jugador_dos)
    return mazo_mesa

def determinar_ganador(rondas, mazo_jugador_uno, mazo_jugador_dos, maximo_rondas_posible: list = 250, rendicion: int = None):

    ganador = None
    mazo_uno = len(mazo_jugador_uno)
    mazo_dos = len(mazo_jugador_dos)

    if mazo_uno == 0:
        ganador = 2
    elif mazo_uno == 0:
        ganador = 1
    elif rondas >= maximo_rondas_posible:
        if mazo_uno > mazo_dos:
            ganador = 1
        elif mazo_uno < mazo_dos:
            ganador = 2
    if rendicion == 1:
        ganador = 2
    elif rendicion == 2:
        ganador = 1
    return ganador

def mostrar_una_carta(pokemon:dict):
    print(f"{pokemon["nombre"]:10} - {pokemon["velocidad"]:3} - {pokemon["fuerza"]:3} - {pokemon["elemento"]:15} - {pokemon["peso"]:5} - {pokemon["altura"]:4}")

def mostrar_lista(lista: list):
    for pokemon in lista:
        mostrar_una_carta(pokemon)

def leer_puntaje_json(path:str)->list:

    with open(path,"r") as archivo_estadisticas:
        puntajes = json.load(archivo_estadisticas)
        
    return puntajes

def cargar_puntaje_a_json(path:str,datos:dict):

    lista_puntajes = []
    lista_puntajes = leer_puntaje_json(path)
    lista_puntajes.append(datos)
    with open(path,"w", encoding="utf8") as archivo_estadisticas:
        json.dump(lista_puntajes,archivo_estadisticas,ensure_ascii=False,indent=4)

def crear_puntaje(ganador: str, cantidad_cartas: int)->dict:
    fecha_actual = str(date.today())
    datos_jugador = {"nombre" : ganador, "puntaje" : cantidad_cartas, "fecha" : fecha_actual}

    return datos_jugador


def mostrar_estadisticas(puntajes:dict):
    for dato in puntajes["estadisticas"]:
        print(f"{dato["nombre"]:10} - {dato["puntaje"]:4} - {dato["fecha"]:12}")

def detectar_rendicion(nombre, jugador):
    jugador_rendido = None
    rendicion = input(f"{nombre}, ¿desea rendirse?: ")
    if rendicion.lower() != "no":
        jugador_rendido = jugador
    return jugador_rendido

def iniciar_juego(path):
        
    rondas = 0
    seguir_jugando = True
    nombre_jugador_uno = asignar_nombres()
    nombre_jugador_dos = asignar_nombres()
    rendicion = False

    ganador_final = None
    lista_cartas = parsear_csv(path)
    minimo_rondas_posible = len(lista_cartas) / 2
    maximo_rondas_posible = len(lista_cartas)

    mezclar_baraja(lista_cartas)

    mazo_jugador_uno = []
    mazo_jugador_dos = []
    mazo_mesa = []
    
    repartir_mazo(lista_cartas,mazo_jugador_uno,mazo_jugador_dos,len(lista_cartas)//2)

    while seguir_jugando:
        atributo = sortear_atributo(mazo_jugador_dos)
        print(f"El atributo elegido es {atributo}")
        system("pause")
        mostrar_una_carta(mazo_jugador_uno[0])
        mostrar_una_carta(mazo_jugador_dos[0])
        time.sleep(3)
        ganador_ronda = comparar_cartas(mazo_jugador_uno, mazo_jugador_dos, atributo)
        if ganador_ronda != None:
            if ganador_ronda:
                ganador = mazo_jugador_uno
                perdedor = mazo_jugador_dos
            else:
                ganador = mazo_jugador_dos
                perdedor = mazo_jugador_uno

            carta_perdedora = perdedor.pop(0)
            ganador.append(carta_perdedora)
            for _ in range(len(mazo_mesa)):
                carta_empatada = mazo_mesa.pop(0)
                ganador.append(carta_empatada)
        else:
            mazo_mesa = llevar_cartas_mesa(mazo_mesa, mazo_jugador_uno, mazo_jugador_dos)
        print(f"El ganador de la ronda es ")
        print(f"Mazo 1: {len(mazo_jugador_uno)} - Mazo 2: {len(mazo_jugador_dos)}")
        # system("pause")
        rondas += 1

        if rondas > 5:
            if len(mazo_jugador_uno) > len(mazo_jugador_dos):
                rendicion = detectar_rendicion(nombre_jugador_dos,2)
    
            elif len(mazo_jugador_uno) < len(mazo_jugador_dos):
                rendicion = detectar_rendicion(nombre_jugador_uno,1)

        if rondas >= minimo_rondas_posible or rendicion == True:
            ganador_final = determinar_ganador(rondas, mazo_jugador_uno, mazo_jugador_dos, maximo_rondas_posible, rendicion)
        elif rondas == maximo_rondas_posible:
            ganador_final = determinar_ganador(rondas, mazo_jugador_uno, mazo_jugador_dos, maximo_rondas_posible)
        if ganador_final is not None or rondas >= maximo_rondas_posible:
            seguir_jugando = False

    if ganador_final == 1:
        nombre_ganador = nombre_jugador_uno
        mazo_ganador = mazo_jugador_uno
    elif ganador_final == 2:
        nombre_ganador = nombre_jugador_dos
        mazo_ganador = mazo_jugador_dos
    else: print("Hubo un empate.")

    print(f"Ganó {nombre_ganador} con {len(mazo_ganador)} cartas.")
    datos_ganador = crear_puntaje(nombre_ganador, len(mazo_ganador))
    cargar_puntaje_a_json("juego_consola/estadisticas.json", datos_ganador)