#Alumnos:
# Motocanchi Huanca, Elvis David
# D'Aragona Agustin Alejandro

import random
import string
import textwrap
import PySimpleGUI as sg  
import Configuracion_sopa
import time
import json
from Raspberry_aplicaciones import registro_ambiental
from Raspberry_Clases import Sonido

def agregar_clase_palabra_horizontal (palabras_lista, cant_palabras, coord_palabras, layout, cant_columas, cant_filas, lista_letras):
	'''Llena las listas del layout con botones que contienen las letras de las palabras despues de agregar una cantidad aleatoria al inicio'''
	for i in range(cant_palabras):
		fila = random.randint(0,cant_filas-1)
		while len(layout[fila]) > 0:
			fila = random.randint(0,cant_filas-1) 
		letras_inicio = random.randint(0,(cant_columas - len(palabras_lista[i])))	
		for j in range(letras_inicio):
			layout[fila].append(sg.Button( random.choice(lista_letras), key = (fila,j), font = 15, button_color = ("black", color_sin_marcar),pad = (0,0)))
		for j in range(letras_inicio, letras_inicio + len(palabras_lista[i])):
			layout[fila].append(sg.Button(palabras_lista[i][j-letras_inicio],key = (fila,j), font = 15, button_color = ("black", color_sin_marcar),pad = (0,0)))
			coord_palabras.append((fila,j))

def convertir_vertical (layout, cant_columnas, cant_filas):
	'''Convierte el layout horizontal a vertical, solo se ejecuta si la casilla "vertical" esta marcada en la configuracion de la sopa'''
	layout_vertical=[]
	for i in range(cant_columnas):
		layout_vertical.append([])
	for columna in range(cant_columnas):
		for fila in range(cant_filas):
			layout_vertical[columna].append(layout[fila][columna])
	return layout_vertical		

def comprobar_palabras (palabras_marcadas, coord_palabras ):
	'''Verifica si los botones marcados con el color de una clase pertenecen a esa clase y si todos las palabras fueron marcadas'''
	if all(elem in palabras_marcadas for elem in coord_palabras):
		if len(coord_palabras) == len(palabras_marcadas):
			aux = True
		else:
			aux = False
	else:
		aux =False
	return aux

def marcar_palabras (palabras_marcadas, coord, palabras_marcadas_2, palabras_marcadas_3, color_marcado, color_sin_marcar): 
	'''Actualiza el color del boton presionado con el color de la clase que esta actualmente seleccionada '''
	if(palabras_marcadas.count(coord)>0) and coord not in (palabras_marcadas_2 + palabras_marcadas_3):
		palabras_marcadas.remove(coord)
		window.Element(coord).Update( button_color =("black",color_sin_marcar))
	elif coord not in (palabras_marcadas_2 + palabras_marcadas_3):
		palabras_marcadas.append(coord)
		window.Element(coord).Update( button_color =("black",color_marcado))

def correccion_cambiar (palabras_marcadas, coord_palabras):
	'''Despues de presionar el boton "comprobar", cambia el color de los botones dependiendo de si fueron marcados correctamente, fueron marcados incorrectamente o faltaron marcarse'''
	for elem in palabras_marcadas:
		if elem in coord_palabras:
			window.Element(elem).Update( button_color =("#ffffff","#36b575"))
		else:
			window.Element(elem).Update( button_color =("#fc5d82","#ea5266"))
	for	elem in set(coord_palabras).difference(palabras_marcadas):
		window.Element(elem).Update( button_color =("#fc5d82","#9DB4A2"))
		
#Programa Principal
# Comienzo del contador para la actualizacion del archivo datos-oficinas.json
tiempo= time.time()
wrapper = textwrap.TextWrapper(width=30) 
diccionario_colores = {"color_sin_marcar": "", "color_marcado":"", "color_sustantivo":"","color_verbo":"","color_adjetivo":""}
tipo_ayuda = {"mostrar_definicion": False, "mostrar_lista": False}
orientacion_vertical =[]
cant_palabras = {"cant_sustantivos":0,"cant_verbos":0,"cant_adjetivos":0}
sopa_mayusculas = []
paleta_colores = {"color_ventana":"","color_letras":"","color_botones":"","color_sopa":""}
oficina_asignada= []

#invocacion a configuracion
diccionario_palabras = Configuracion_sopa.Ingreso_de_palabras ()		
cant_palabras_default = [len(list(diccionario_palabras["NN"].keys())),len(list(diccionario_palabras["VB"].keys())),len(list(diccionario_palabras["JJ"].keys()))]
Configuracion_sopa.configurar_sopa(diccionario_colores, tipo_ayuda,orientacion_vertical,cant_palabras,sopa_mayusculas,cant_palabras_default,oficina_asignada)
orientacion = orientacion_vertical[0]
oficina= oficina_asignada[0]

#Lectura del archivo Json de temperatura y humedad:
archivo = open("Json_files/datos-oficinas.json", "r")
datos_json = json.load(archivo)
archivo.close()
total= len(datos_json[oficina])
promedio_temp= 0
promedio_hum= 0
for j in range(len(datos_json[oficina])):
	promedio_temp= promedio_temp + datos_json[oficina][j]['temperatura']
	promedio_hum= promedio_hum + datos_json[oficina][j]['humedad']
promedio_temp= promedio_temp / total
promedio_hum= promedio_hum / total

#Cambiando look and feel acordingly:
if promedio_temp < 10:
	color_fondo = "#dff0ea"
	color_secun = "#574f7d"
	color_sin_marcar = "#95adbe"
	color_boton = "#343975"

elif promedio_temp > 30:
	color_fondo = "#C14A6A"
	color_secun = "#eb5f5d"
	color_sin_marcar = "#fabc74"
	color_boton = "#239f95"

else:
	color_fondo = "#b8e9c0"
	color_secun = "#6384b3"
	color_sin_marcar = "#e6f0b6"
	color_boton = "#684949"

#Lista random de las palabras 
cant_sustantivos =int(cant_palabras["cant_sustantivos"])
if cant_sustantivos > len(diccionario_palabras["NN"]):
	cant_sustantivos = len(diccionario_palabras["NN"])
cant_verbos =int(cant_palabras["cant_verbos"])
if cant_verbos > len(diccionario_palabras["VB"]):
	cant_verbos = len(diccionario_palabras["VB"])
cant_adjetivos = int(cant_palabras["cant_adjetivos"])
if cant_adjetivos > len(diccionario_palabras["JJ"]):
	cant_adjetivos = len(diccionario_palabras["JJ"])
	
sustantivos_lista = random.sample(list(diccionario_palabras["NN"].keys()),cant_sustantivos)
verbos_lista = 		random.sample(list(diccionario_palabras["VB"].keys()),cant_verbos)
adjetivos_lista = 	random.sample(list(diccionario_palabras["JJ"].keys()),cant_adjetivos)
 


color_marcado_sustantivo = diccionario_colores["color_sustantivo"]
color_marcado_verbo= diccionario_colores["color_verbo"]
color_marcado_adjetivo = diccionario_colores["color_adjetivo"]

#Opciones para el estilo de la sopa de letras
sg.SetOptions(button_element_size=(4, 2), auto_size_buttons=False, background_color = color_fondo)	

#Mayusculas o minusculas:
if sopa_mayusculas[0]:
	lista_letras = string.ascii_uppercase
	sustantivos_lista_sopa = list(map(lambda x: x.upper() , sustantivos_lista))	
	verbos_lista_sopa = list(map(lambda x: x.upper() , verbos_lista))	
	adjetivos_lista_sopa = list(map(lambda x: x.upper() , adjetivos_lista))	
else:
	sustantivos_lista_sopa = sustantivos_lista	
	verbos_lista_sopa = verbos_lista	
	adjetivos_lista_sopa = adjetivos_lista
	lista_letras = string.ascii_lowercase

largo_min = max(len(max(sustantivos_lista, key=len))if len(sustantivos_lista) != 0 else 0,
				len(max(verbos_lista, key=len))if len(verbos_lista) != 0 else 0,
				len(max(adjetivos_lista, key=len))if len(adjetivos_lista) != 0 else 0)
alto_min = cant_sustantivos + cant_adjetivos + cant_verbos

cant_filas =  	3 if alto_min < 3 else alto_min + random.randint(0,int(alto_min/2))
cant_columas = 	largo_min + random.randint(0,int(largo_min/2))

#listas vacias en las que se agregara informacion con .append()
layout_sopa = [[]]
coord_sustantivos =[]
coord_verbos =[]
coord_adjetivos =[]
sustantivos_marcados =[]
verbos_marcados =[]
adjetivos_marcados =[]

#creando una lista vacia por cada fila en el layout 
for i in range (cant_filas):
	row = []
	layout_sopa.append(row)
	
if cant_sustantivos>0:
	agregar_clase_palabra_horizontal(sustantivos_lista_sopa, cant_sustantivos,coord_sustantivos , 	layout_sopa, cant_columas, cant_filas,lista_letras) 
if cant_verbos>0:
	agregar_clase_palabra_horizontal(verbos_lista_sopa,	  cant_verbos,coord_verbos,			 		layout_sopa, cant_columas, cant_filas,lista_letras)
if cant_adjetivos>0:  
	agregar_clase_palabra_horizontal(adjetivos_lista_sopa,   cant_adjetivos,coord_adjetivos, 		layout_sopa, cant_columas, cant_filas,lista_letras) 

#Agregando letras faltantes por cada fila
for fila in range (cant_filas):
	if len(layout_sopa[fila]) < cant_columas:
		fila_llena = len(layout_sopa[fila])
		letras_faltantes = cant_columas - len(layout_sopa[fila])
		for j in range (letras_faltantes):
			layout_sopa[fila].append(sg.Button( random.choice(lista_letras), font = 15, key = (fila,j+fila_llena), button_color = ("black", color_sin_marcar),pad = (0,0)))
#Cambiando la orientacion si es que se marco la opcion vertical
if not orientacion:
	layout_sopa = convertir_vertical(layout_sopa,cant_columas, cant_filas) 

#Lista de definiciones de palabras:
lista_ayuda = []
if tipo_ayuda["mostrar_definicion"] and not tipo_ayuda["mostrar_lista"]:
	sustantivos_ayuda =[]
	for i in sustantivos_lista:
		sustantivos_ayuda.append([sg.Text("- "+ wrapper.fill(diccionario_palabras["NN"][i]),background_color =color_secun,text_color = "snow")])
	verbos_ayuda =[]
	for i in verbos_lista:
		verbos_ayuda.append([sg.Text("- "+ wrapper.fill(diccionario_palabras["VB"][i]),background_color =color_secun,text_color = "snow")])
	adjetivos_ayuda =[]
	for i in adjetivos_lista:
		adjetivos_ayuda.append([sg.Text("- "+ wrapper.fill(diccionario_palabras["JJ"][i]),background_color =color_secun,text_color = "snow")])
		
elif tipo_ayuda["mostrar_lista"] and not tipo_ayuda["mostrar_definicion"]:
	sustantivos_ayuda =[]
	for i in sustantivos_lista:
		sustantivos_ayuda.append([sg.Text("- " + i.upper(),background_color =color_secun,text_color = "snow")])
	verbos_ayuda =[]
	for i in verbos_lista:
		verbos_ayuda.append([sg.Text("- " + i.upper(),background_color =color_secun,text_color = "snow")])
	adjetivos_ayuda =[]
	for i in adjetivos_lista:
		adjetivos_ayuda.append([sg.Text("- " + i.upper(),background_color =color_secun,text_color = "snow")])
	
elif tipo_ayuda["mostrar_definicion"] and tipo_ayuda["mostrar_lista"]:
	sustantivos_ayuda =[]
	for i in sustantivos_lista:
		sustantivos_ayuda.append([sg.Text("- " + wrapper.fill(i.upper() +": "+diccionario_palabras["NN"][i]),background_color =color_secun,text_color = "snow")])
	verbos_ayuda =[]
	for i in verbos_lista:
		verbos_ayuda.append([sg.Text("- " + wrapper.fill(i.upper()+": "+diccionario_palabras["VB"][i]),background_color =color_secun,text_color = "snow")])
	adjetivos_ayuda =[]
	for i in adjetivos_lista:
		adjetivos_ayuda.append([sg.Text("- " + wrapper.fill(i.upper()+": "+diccionario_palabras["JJ"][i]),background_color =color_secun,text_color = "snow")])
	
elif 	not tipo_ayuda["mostrar_definicion"] and not tipo_ayuda["mostrar_lista"]:
	sustantivos_ayuda = [[sg.Text("Cantidad = "+ str(cant_sustantivos),background_color =color_secun,text_color = "snow")]]
	verbos_ayuda = [[sg.Text("Cantidad = "+str(cant_verbos),background_color =color_secun,text_color = "snow")]]
	adjetivos_ayuda = [[sg.Text("Cantidad = "+str(cant_adjetivos),background_color =color_secun,text_color = "snow")]]
	
#Definiendo el layout	
lista_ayuda.append([sg.Frame("Sustantivos:",sustantivos_ayuda, background_color =color_secun,title_color='snow')])
lista_ayuda.append([sg.Frame("Verbos:",verbos_ayuda, background_color =color_secun,title_color='snow')])
lista_ayuda.append([sg.Frame("Adjetivos:",adjetivos_ayuda, background_color =color_secun,title_color='snow')])

columna_ayuda = [[sg.Frame('Ayuda:',lista_ayuda, title_color = "snow",background_color =color_secun)]]

columna_seleccion_tipo = [[sg.Text('Opciones ',background_color =color_secun,text_color='snow',  justification='center', size=(10, 1))],      
               [sg.Radio('Sustantivo', "clase_palabra",key = "sustantivo_radio",size=(10, 15),font = 25,text_color = "grey15" ,background_color = diccionario_colores["color_sustantivo"], default=True )],
               [sg.T(' ', background_color = color_secun)], [sg.Radio('Verbo', "clase_palabra",key = "verbo_radio",			size=(10, 15),font = 25,text_color = "grey15" ,background_color = diccionario_colores["color_verbo"] )],
               [sg.T(' ', background_color = color_secun)], [sg.Radio('Adjetivo', "clase_palabra",key = "adjetivo_radio", 	size=(10, 15),font = 25,text_color = "grey15" ,background_color = diccionario_colores["color_adjetivo"] )],
               [sg.T(' ', background_color = color_secun)], [sg.Button("Comprobar", key = "comprobar_boton", button_color = ("snow",color_boton),size=(14, 3),pad=(5,5) )],
               [sg.T(' ', background_color = color_secun)], [sg.T(' ', background_color = color_secun)], [sg.T(' ', background_color = color_secun ), sg.OK("Reiniciar",button_color=("#ffffff",color_boton),size=(10,2),pad=(5,5))],
               [sg.T(' ', background_color = color_secun)], [sg.T(' ', background_color = color_secun)], [sg.T(' ', background_color = color_secun ), sg.Exit(button_color=("#ffffff",color_boton),size=(10,2),pad=(5,5))]]

layout = [[sg.Column(columna_ayuda),sg.Frame('Sopa De Letras', layout_sopa,background_color = color_secun,title_color = "snow"),sg.Column(columna_seleccion_tipo, background_color=color_secun)]]

window = sg.Window('Mi Sopa de Letras', layout)  
# Evento Sopa de letras:
sensor= Sonido()
while True:
	event, values = window.Read(timeout=20)
	
	# Actualizando el archivo json cada 1 minuto
	if (time.time() - tiempo) > 60:
		registro_ambiental(oficina)
		tiempo= time.time()
	
	# Verificando si hubo algun sonido en el microfono
	sensor.evento_detectado(muestra_datos,[promedio_temp,promedio_hum])
	
	#Marcando las palabras con el color correspondiente:
	if type(event) is tuple: 
		if(values["sustantivo_radio"]):
			marcar_palabras(sustantivos_marcados, event, verbos_marcados, adjetivos_marcados, color_marcado_sustantivo, color_sin_marcar)
	
		elif(values["verbo_radio"]):
			marcar_palabras(verbos_marcados, event, sustantivos_marcados, adjetivos_marcados, color_marcado_verbo, color_sin_marcar)
			
		elif (values["adjetivo_radio"]):
			marcar_palabras(adjetivos_marcados, event, verbos_marcados, sustantivos_marcados, color_marcado_adjetivo, color_sin_marcar)
	#Boton Salir:		
	if event == 'Exit':  
		break  
		
	#Boton Reiniciar:
	if event is "Reiniciar":
		for i in range(cant_filas):
			for j in range(cant_columas):
				window.Element((i , j)).Update(disabled=False, button_color =("black", color_sin_marcar))
				sustantivos_marcados.clear()
				verbos_marcados.clear()
				adjetivos_marcados.clear()
	#Boton Comprobar:
	elif event is "comprobar_boton":
		#Desabilitando los botones ( el juego termino )
		for i in range(cant_filas):
			for j in range(cant_columas):
				window.Element((i , j)).Update(disabled=True)
		
		#Comprobar palabras
		sustantivos_correctos = False
		verbos_correctos = False
		adjetivos_correctos = False
								
		#Comprobar palabras
		sustantivos_correctos = comprobar_palabras(sustantivos_marcados,coord_sustantivos)	
		verbos_correctos = comprobar_palabras(verbos_marcados,coord_verbos)	
		adjetivos_correctos = comprobar_palabras(adjetivos_marcados,coord_adjetivos)	
			
		#Marcar elementos correctos e incorrectos en la grilla
		correccion_cambiar(sustantivos_marcados, coord_sustantivos)
		correccion_cambiar(verbos_marcados, coord_verbos)
		correccion_cambiar(adjetivos_marcados, coord_adjetivos)
		
		#ventana con el resultado
		if sustantivos_correctos and verbos_correctos and adjetivos_correctos:
			window_final = sg.Window('Mi Sopa de Letras', 	[[sg.Text("¡Felicidades! Completaste la sopa de letras correctamente.",background_color = "grey20",text_color = "snow",font=20)],
															[sg.T(' '*30, background_color = color_fondo), sg.CloseButton ("OK", button_color =("snow","#3698A9"),size=(15,2))]]) 
		else:
			window_final = sg.Window('Mi Sopa de Letras', 	[[sg.Text("¡Que pena! Deberias intentarlo denuevo.",background_color = "grey20",text_color = "snow",font=20)],
															[sg.T(' '*16, background_color = color_fondo),sg.CloseButton ("OK", button_color =("snow","#3698A9"),size=(15,2))]]) 
		event, values = window_final.Read()
		

		
			
# ~ window.Close()
