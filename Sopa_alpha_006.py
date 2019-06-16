import sys  
import random
import string
import textwrap
if sys.version_info[0] >= 3:  
    import PySimpleGUI as sg  
else:  
    import PySimpleGUI27 as sg  
import Configuracion_sopa

def agregar_clase_palabra_horizontal (palabras_lista, cant_palabras, coord_palabras, layout, cant_columas, cant_filas):
	for i in range(cant_palabras):
		fila = random.randrange(cant_filas)
		while len(layout[fila]) > 0:
			fila = random.randrange(cant_filas) 
		letras_inicio = random.randrange(cant_columas - len(palabras_lista[i]))	
		for j in range(letras_inicio):
			layout[fila].append(sg.Button( random.choice(string.ascii_letters).upper(), key = (fila,j), font = 15, button_color = ("black", color_sin_marcar),pad = (0,0)))
		for j in range(letras_inicio, letras_inicio + len(palabras_lista[i])):
			layout[fila].append(sg.Button(palabras_lista[i][j-letras_inicio].upper(),key = (fila,j), font = 15, button_color = ("black", color_sin_marcar),pad = (0,0)))
			coord_palabras.append((fila,j))

def convertir_vertical (layout, cant_columnas, cant_filas):
	layout_vertical=[]
	for i in range(cant_columnas):
		layout_vertical.append([])
	for columna in range(cant_columnas):
		for fila in range(cant_filas):
			layout_vertical[columna].append(layout[fila][columna])
	return layout_vertical		

#Programa Principal
wrapper = textwrap.TextWrapper(width=50) 
diccionario_colores = {"color_sin_marcar": "", "color_marcado":"", "color_sustantivo":"","color_verbo":"","color_adjetivo":""}
tipo_ayuda = {"mostrar_definicion": False, "mostrar_lista": False}
orientacion_vertical =[]
cant_palabras = {"cant_sustantivos":0,"cant_verbos":0,"cant_adjetivos":0}
sopa_mayusculas = []
paleta_colores = {"color_ventana":"","color_letras":"","color_botones":"","color_sopa":""}

#invocacion a configuracion
Configuracion_sopa.configurar_sopa(diccionario_colores, tipo_ayuda,orientacion_vertical,cant_palabras,sopa_mayusculas)
diccionario_palabras = Configuracion_sopa.Ingreso_de_palabras ()		

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
verbos_lista = random.sample(list(diccionario_palabras["VB"].keys()),cant_verbos)
adjetivos_lista = random.sample(list(diccionario_palabras["JJ"].keys()),cant_adjetivos)
 
vertical = not orientacion_vertical[0]
color_sin_marcar = "grey35"
color_marcado_sustantivo = diccionario_colores["color_sustantivo"]
color_marcado_verbo= diccionario_colores["color_verbo"]
color_marcado_adjetivo = diccionario_colores["color_adjetivo"]

#Variable Vertical
# ~ lista_letras_mayusculas=[]
# ~ lista_letras_minusculas=[]
	
#if sopa_mayusculas[0]:
	#usar upper con map y lambda
	# ~ sustantivos_lista = list(sustantivos.keys())
	# ~ verbos_lista = list(verbos.keys())
	# ~ adjetivos_lista = list(adjetivos.keys())
	# ~ lista_letras = lista_letras_mayusculas


#Horizontal

largo_min = max(len(max(sustantivos_lista,key=len)),len(max(verbos_lista,key=len)),len(max(adjetivos_lista,key=len)))
alto_min = cant_sustantivos + cant_adjetivos + cant_verbos

cant_filas = alto_min +3
cant_columas = largo_min + 4

layout_sopa = []
coord_sustantivos =[]
coord_verbos =[]
coord_adjetivos =[]
#Opciones para el estilo de la sopa de letras
sg.SetOptions(button_element_size=(4, 2), auto_size_buttons=False,background_color="grey20")	
for i in range (cant_filas):
	row = []
	layout_sopa.append(row)
	
agregar_clase_palabra_horizontal(sustantivos_lista, cant_sustantivos,coord_sustantivos , layout_sopa, cant_columas, cant_filas)
agregar_clase_palabra_horizontal(verbos_lista,	 cant_verbos,coord_verbos, layout_sopa, cant_columas, cant_filas)
agregar_clase_palabra_horizontal(adjetivos_lista, cant_adjetivos,coord_adjetivos, layout_sopa, cant_columas, cant_filas)

print(coord_sustantivos)
print(coord_verbos)
print(coord_adjetivos)

for fila in range (cant_filas):
	if len(layout_sopa[fila]) < cant_columas:
		fila_llena = len(layout_sopa[fila])
		letras_faltantes = cant_columas - len(layout_sopa[fila])
		for j in range (letras_faltantes):
			layout_sopa[fila].append(sg.Button( random.choice(string.ascii_letters).upper(), font = 15, key = (fila,j+fila_llena), button_color = ("black", color_sin_marcar),pad = (0,0)))

if vertical:
	layout_sopa = convertir_vertical(layout_sopa,cant_columas, cant_filas) 

sustantivos_marcados =[]
verbos_marcados =[]
adjetivos_marcados =[]

#Lista de definiciones de palabras:
lista_ayuda = []
if tipo_ayuda["mostrar_definicion"] and not tipo_ayuda["mostrar_lista"]:
	sustantivos_definiciones =[]
	for i in sustantivos_lista:
		sustantivos_definiciones.append([sg.Text("- "+ wrapper.fill(diccionario_palabras["NN"][i]))])
	verbos_definiciones =[]
	for i in verbos_lista:
		verbos_definiciones.append([sg.Text("- "+ wrapper.fill(diccionario_palabras["VB"][i]))])
	adjetivos_definiciones =[]
	for i in adjetivos_lista:
		adjetivos_definiciones.append([sg.Text("- "+ wrapper.fill(diccionario_palabras["JJ"][i]))])
	lista_ayuda.append([sg.Frame("Sustantivos:",sustantivos_definiciones)])
	lista_ayuda.append([sg.Frame("Verbos:",verbos_definiciones)])
	lista_ayuda.append([sg.Frame("Adjetivos:",adjetivos_definiciones)])
			
if tipo_ayuda["mostrar_lista"] and not tipo_ayuda["mostrar_definicion"]:
	sustantivos_ayuda =[]
	for i in sustantivos_lista:
		sustantivos_ayuda.append([sg.Text("- " + i).upper()])
	verbos_ayuda =[]
	for i in verbos_lista:
		verbos_ayuda.append([sg.Text("- " + i).upper()])
	adjetivos_ayuda =[]
	for i in adjetivos_lista:
		adjetivos_ayuda.append([sg.Text("- " + i).upper()])
	lista_ayuda.append([sg.Frame("Sustantivos:",sustantivos_ayuda)])
	lista_ayuda.append([sg.Frame("Verbos:",verbos_ayuda)])
	lista_ayuda.append([sg.Frame("Adjetivos:",adjetivos_ayuda)])
	
if tipo_ayuda["mostrar_definicion"] and tipo_ayuda["mostrar_lista"]:
	sustantivos_definiciones =[]
	for i in sustantivos_lista:
		sustantivos_definiciones.append([sg.Text("- " + wrapper.fill(i.upper() +": "+diccionario_palabras["NN"][i]))])
	verbos_definiciones =[]
	for i in verbos_lista:
		verbos_definiciones.append([sg.Text("- " + wrapper.fill(i.upper()+": "+diccionario_palabras["VB"][i]))])
	adjetivos_definiciones =[]
	for i in adjetivos_lista:
		adjetivos_definiciones.append([sg.Text("- " + wrapper.fill(i.upper()+": "+diccionario_palabras["JJ"][i]))])
	
	lista_ayuda.append([sg.Frame("Sustantivos:",sustantivos_definiciones)])
	lista_ayuda.append([sg.Frame("Verbos:",verbos_definiciones)])
	lista_ayuda.append([sg.Frame("Adjetivos:",adjetivos_definiciones)])

if 	not tipo_ayuda["mostrar_definicion"] and not tipo_ayuda["mostrar_lista"]:
	lista_ayuda.append([sg.Text("No selecciono ninguno de los modos de ayuda")])

columna_ayuda = [[sg.Frame('Ayuda:',lista_ayuda)]]

columna_seleccion_tipo = [[sg.Text('Opciones ',background_color ="grey20",  justification='center', size=(10, 1))],      
               [sg.Radio('Sustantivo', "clase_palabra",key = "sustantivo_radio",size=(10, 15),font = 25,text_color = "grey15" ,background_color = diccionario_colores["color_sustantivo"], default=True )],
               [sg.Radio('Verbo', "clase_palabra",key = "verbo_radio",			size=(10, 15),font = 25,text_color = "grey15" ,background_color = diccionario_colores["color_verbo"] )],
               [sg.Radio('Adjetivo', "clase_palabra",key = "adjetivo_radio", 	size=(10, 15),font = 25,text_color = "grey15" ,background_color = diccionario_colores["color_adjetivo"] )],
               [sg.Button("Comprobar", key = "comprobar_boton", button_color = ("black","LightSkyBlue2"),size=(20, 10),pad=(10,10) )],
               [sg.Exit(button_color=("black","LightSkyBlue2"),pad=(60,50))]]

layout = [[sg.Column(columna_ayuda),sg.Frame('Sopa De Letras', layout_sopa,background_color = "grey20"),sg.Column(columna_seleccion_tipo, background_color='grey20')]]


window = sg.Window('Mi Sopa de Letras', layout)  

while True:                 # Event Loop  
	event, values = window.Read()  
	
	
	print(event, values)
	# ~ print(type(event), type(values))
	
	if event is None or event == 'Exit':  
		break  
	if event is "comprobar_boton":
		if all(elem in sustantivos_marcados for elem in coord_sustantivos):
			if len(coord_sustantivos) == len(sustantivos_marcados):
				print("Sustantivos Correctos")
			else:
				print("Sustantivos Incorrectos")
		else:
			print("Adjetivos Incorrectos")	 
					
		if all (elem in verbos_marcados for elem in coord_verbos):
			if len(coord_verbos) == len(verbos_marcados):
				print("Verbos Correctos")
			else:
				print("Verbos Incorrectos")	
		else:
			print("Adjetivos Incorrectos")	 
					
		if all (elem in adjetivos_marcados for elem in coord_adjetivos):
			if len(coord_adjetivos) == len(adjetivos_marcados):
				print("Adjetivos Correctos")
			else:
				print("Adjetivos Incorrectos")		
		else:
			print("Adjetivos Incorrectos")	 
		# ~ print("sustantivos: ",sustantivos_marcados)
		# ~ print("verbos: " , verbos_marcados)
		# ~ print("adjetivos: ", adjetivos_marcados)
	else:
		if(values["sustantivo_radio"]):
			if(sustantivos_marcados.count(event)>0):
				sustantivos_marcados.remove(event)
				window.Element(event).Update( button_color =("black",color_sin_marcar))
			else:
				sustantivos_marcados.append(event)
				window.Element(event).Update( button_color =("black",color_marcado_sustantivo))
		elif(values["verbo_radio"]):
			if(verbos_marcados.count(event)>0):
				verbos_marcados.remove(event)
				window.Element(event).Update( button_color =("black",color_sin_marcar))
			else:
				verbos_marcados.append(event)
				window.Element(event).Update( button_color =("black",color_marcado_verbo))
		elif (values["adjetivo_radio"]):
			if(adjetivos_marcados.count(event)>0):
				adjetivos_marcados.remove(event)
				window.Element(event).Update( button_color =("black",color_sin_marcar))
			else:
				adjetivos_marcados.append(event)
				window.Element(event).Update( button_color =("black",color_marcado_adjetivo))
window.Close()
