def Ingreso_de_palabras():
	# Permite el ingreso de palabras y las busca
	# en Wikcionario junto con su definicion, si esta entonces guarda
	# las palabra junto con sus definicion en un diccionario que tiene como
	# claves el tipo de palabra y como valor otro diccionario
	# que contiene a las palabras como claves y a sus definiciones
	# como valor; si la palabra no esta en Wikcionario entonces
	# crea un archivo txt con el reporte de las palabras que no esten
	# y se ingresa la palabra con el tipo que te diga pattern y la
	# definicion ingresada por el usuario
	
	from pattern.web import Wiktionary
	from pattern.es import parse, split, singularize
	import PySimpleGUI as sg
	wiki= Wiktionary(language= "es")
	dic= {'NN':{},'VB':{},'JJ':{}}
	disenio1 =[[sg.Text('Ingrese un sustantivo, verbo o adjetivo para agregar a las palabras de la sopa de letras'), sg.InputText(do_not_clear=False, key= 'palabra')],
			[sg.Button("Agregar"), sg.Button("Listo")]]
	ventana1= sg.Window('Ingreso de palabras').Layout(disenio1)
	arch= open('reporte.txt','w')
	arch.close()
	while True:
		boton, values1= ventana1.Read()
		if boton is None or boton == 'Listo':
			break
		else:
			palabra= values1['palabra']
			palabra= singularize(palabra)
			articulo= wiki.search(palabra)
			try:
				secciones= articulo.sections
				pos= 0
				#Verificacion de cual seccion tiene la informacion del tipo y definicion de la palabra ingresada
				while(not secciones[pos].title.startswith(('Sus','Ver','Ad','For')) and pos < len(secciones)- 1):
					pos= pos + 1
				seccion= secciones[pos]
				lista_seccion= seccion.string.split('\n')
				if seccion.title.startswith('Sustantivo'):
					tipo= 'NN'
					pos= 7
				elif seccion.title.startswith('Verbo') or 'verbal' in seccion.title:
					tipo= 'VB'
					pos= 2
				elif seccion.title.startswith('Adjetivo') or 'adjetiva' in seccion.title:
					tipo= 'JJ'
					pos= 10 if seccion.title.startswith('Adjetivo') else 2
				#Se busca la 1era definicion de la palabra
				while(not lista_seccion[pos].startswith('1')):
					pos= pos + 1
				definicion= lista_seccion[pos][1:]
				if tipo != parse(palabra).split('/')[1]:
					reporte= 'El tipo de '+ palabra +' que indica Wikcionario no coincide con el tipo que indica pattern'
					arch= open('reporte.txt','a')
					arch.write('-'+reporte+'\n')
					arch.close()
				dic[tipo][palabra]= definicion
			except AttributeError:
				reporte= palabra +' no se encuentra en Wikcionario'
				arch= open('reporte.txt','a')
				arch.write('-'+reporte+'\n')
				arch.close()
				tipo= parse(palabra).split('/')[1]
				disenio2 =[[sg.Text('La palabra no esta en Wikcionario')],
							[sg.Text('Ingrese una definicion para la palabra '+ palabra), sg.InputText(do_not_clear=False, key= 'definicion')],
							[sg.Button("Agregar")]]
				ventana2= sg.Window('Ingreso de definicion').Layout(disenio2)
				boton, values2= ventana2.Read()
				definicion= values2['definicion']
				dic[tipo][palabra]= definicion
				ventana2.Close()
	ventana1.Close()
	print('NN:',dic['NN'])
	print()
	print('VB:',dic['VB'])
	print()
	print('JJ:',dic['JJ'])
	return dic
	
def configurar_sopa(diccionario_colores, tipo_ayuda,orientacion_vertical,cant_palabras,sopa_mayusculas):
	# Establece la configuracion de la sopa de letras
	# devolviendo los valores ingresados en estructuras de datos.
	# En caso de que los colores se repitan se abre una ventana para avisar de esto.
	import PySimpleGUI as sg
	dic= {'Negro':'black','Gris':'gray','Blanco':'white','Rojo':'#f94a4f','Naranja':'#f29646','Dorado':'gold','Plateado':'silver','Amarillo':'#f9e54a','Verde':'green','Cyan':'#2dc7e2','Azul':'#478de8','Purpura':'#9453c6','Magenta':'#dc6be0','Rosa':'#f78383'}
	
	elegir_color = [[sg.Text('Ingrese un color para los sustantivos'), sg.InputCombo(['Negro','Gris','Blanco','Rojo','Naranja','Dorado','Plateado','Amarillo','Verde','Cyan','Azul','Purpura','Magenta','Rosa'],default_value='Rojo', key= 'color_sustantivo')],
					[sg.Text('Ingrese un color para los verbos'), sg.InputCombo(['Negro','Gris','Blanco','Rojo','Naranja','Dorado','Plateado','Amarillo','Verde','Cyan','Azul','Purpura','Magenta','Rosa'],default_value='Amarillo', key= 'color_verbo')],
					[sg.Text('Ingrese un color para los adjetivos'), sg.InputCombo(['Negro','Gris','Blanco','Rojo','Naranja','Dorado','Plateado','Amarillo','Verde','Cyan','Azul','Purpura','Magenta','Rosa'],default_value='Verde', key= 'color_adjetivo')]]
	
	elegir_ayuda = [[sg.Checkbox('Mostrar las definiciones de las palabras',key= 'mostrar_def')], 
					[sg.Checkbox('Mostrar la lista de palabras a buscar',key= 'mostrar_lista')]]
	
	elegir_orientacion = [[sg.Radio('Horizontal', "RADIO1",default=True,key= 'hor'), sg.Radio('Vertical', "RADIO1",key= 'vert')]]
	
	elegir_cant_palabras = [[sg.Text('Sustantivos'), sg.Input(1,key= 'cant_sus')],
							[sg.Text('Verbos'), sg.Input(1,key= 'cant_ver')],
							[sg.Text('Adjetivos'), sg.Input(1,key= 'cant_adj')]]
	
	elegir_mayus_minus = [[sg.Radio('Mayuscula', "RADIO2",default=True,key= 'mayus'), sg.Radio('Minuscula', "RADIO2",key= 'minus')]]
	
	configuracion= [[sg.Frame('Colores', elegir_color)],
					[sg.Frame('Tipo de ayuda', elegir_ayuda)],
					[sg.Frame('Orientacion de las palabras', elegir_orientacion)],
					[sg.Frame('Cantidad a mostrar', elegir_cant_palabras)],
					[sg.Frame('Tipo de letra de la sopa de letras', elegir_mayus_minus)],
					[sg.Button("Listo")]]
	ventana= sg.Window('Configuracion',resizable=True).Layout(configuracion)
	while True:
		boton, values= ventana.Read()
		if boton is None:
			break
		if boton == 'Listo':
			#Condicion para que no se repitan los colores
			if (values['color_sustantivo'] != values['color_verbo']) and (values['color_sustantivo'] != values['color_adjetivo']) and (values['color_verbo'] != values['color_adjetivo']):
				break
			else:
				sg.PopupOK('Los colores de las palabras deben ser distintos!',grab_anywhere=True)
	ventana.Close()
	diccionario_colores["color_sustantivo"]= dic[values['color_sustantivo']]
	diccionario_colores["color_verbo"]= dic[values['color_verbo']]
	diccionario_colores["color_adjetivo"]= dic[values['color_adjetivo']]
	tipo_ayuda["mostrar_definicion"]= values['mostrar_def']
	tipo_ayuda["mostrar_lista"]= values['mostrar_lista']
	orientacion_vertical.append(values["hor"])
	cant_palabras["cant_sustantivos"]= values['cant_sus']
	cant_palabras["cant_verbos"]= values['cant_ver']
	cant_palabras["cant_adjetivos"]= values['cant_adj']
	sopa_mayusculas.append(values["mayus"])
	
# ~ dic= Ingreso_de_palabras()
# ~ print()
# ~ print(dic)
# ~ diccionario_colores = {"color_sin_marcar": "", "color_marcado":"", "color_sustantivo":"","color_verbo":"","color_adjetivo":""}
# ~ tipo_ayuda = {"mostrar_definicion": False, "mostrar_lista": False}
# ~ orientacion_vertical =[]
# ~ cant_palabras = {"cant_sustantivos":0,"cant_verbos":0,"cant_adjetivos":0}
# ~ sopa_mayusculas = []
# ~ #invocacion a configuracion
# ~ configurar_sopa(diccionario_colores, tipo_ayuda,orientacion_vertical,cant_palabras,sopa_mayusculas)
# ~ print(diccionario_colores)
# ~ print()
# ~ print(tipo_ayuda)
# ~ print()
# ~ print(orientacion_vertical)
# ~ print()
# ~ print(cant_palabras)
# ~ print()
# ~ print(sopa_mayusculas)
