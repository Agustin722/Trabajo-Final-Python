#Alumnos:
# Motocanchi Huanca, Elvis David
# D'Aragona Agustin Alejandro

def cambiar_apariencia_ventana():
	''' Realiza el cambio del "look and feel" de la ventana
	con la informacion de las "oficinas" del archivo json
	y devuelve la lista de oficinas de las que se elige
	una en la configuracion
	'''
	import PySimpleGUI as sg
	import json
	
	arch= open('Json_files/datos-oficinas.json', 'r')
	dic_temp_hum= json.load(arch)
	arch.close()
	total= 0
	prom= 0
	for i in dic_temp_hum.keys():
		total= total + len(dic_temp_hum[i])
		for j in range(len(dic_temp_hum[i])):
			prom= prom + dic_temp_hum[i][j]['temperatura']
	prom= prom / total
	if prom < 10:
		sg.ChangeLookAndFeel('GreenTan')
	elif prom > 30:
		sg.ChangeLookAndFeel('BluePurple')
	else:
		sg.ChangeLookAndFeel('BluePurple')
	return list(dic_temp_hum.keys())

def Ingreso_de_palabras():
	''' Permite el ingreso de palabras y las busca
	en Wikcionario junto con su definicion, si esta entonces guarda
	las palabra junto con sus definicion en un diccionario que tiene como
	claves el tipo de palabra y como valor otro diccionario
	que contiene a las palabras como claves y a sus definiciones
	como valor; si la palabra no esta en Wikcionario entonces
	crea un archivo txt con el reporte de las palabras que no esten
	y se ingresa la palabra con el tipo que te diga pattern y la
	definicion ingresada por el usuario
	'''
	from pattern.web import Wiktionary
	from pattern.es import parse, split, singularize
	import PySimpleGUI as sg
	
	sg.SetOptions(button_element_size=(4, 2), background_color = "grey20")
	cambiar_apariencia_ventana()
	wiki= Wiktionary(language= "es")
	dic= {'NN':{},'VB':{},'JJ':{}}
	disenio1 =[[sg.Text('Ingrese un sustantivo, verbo o adjetivo para \nagregar a las palabras de la sopa de letras',background_color = "grey20",text_color = "snow"), sg.InputText(do_not_clear=False, key= 'palabra',background_color = "grey35",text_color = "snow",size=(35,1))],
			[sg.T(" ", background_color = "grey20" )],
			[sg.Output(size=(70,3), key= 'muestra',background_color = "grey35",text_color = "snow")],
			[sg.T(" ", background_color = "grey20" )],
			[sg.T(" "*20, background_color = "grey20" ), sg.Button("Agregar", size =(10,2) , button_color = ("#ffffff","#3698A9")), sg.T(" "*25, background_color = "grey20"), sg.Button("Listo",size =(10,2) , button_color = ("#ffffff","#3698A9"))]]
	ventana1= sg.Window('Ingreso de palabras').Layout(disenio1)
	arch= open('reporte.txt','w')
	arch.close()
	sustantivos= []
	verbos= []
	adjetivos= []
	while True:
		boton, values1= ventana1.Read()
		if boton is None:
			break
		elif boton == 'Listo':
			if(len(sustantivos) != 0 or len(verbos) != 0 or len(adjetivos) != 0):
				break
			else:
				sg.PopupOK('Error 420, Ingrese al menos una palabra de los tipos pedidos',grab_anywhere=True)
		else:
			palabra= values1['palabra']
			if palabra != '' and not palabra.startswith(' ') and not palabra.endswith(' '):
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
						if not(palabra in sustantivos):
							sustantivos.append(palabra)
						pos= 7
					elif seccion.title.startswith('Verbo') or 'verbal' in seccion.title:
						tipo= 'VB'
						if not(palabra in verbos):
							verbos.append(palabra)
						pos= 2
					elif seccion.title.startswith('Adjetivo') or 'adjetiva' in seccion.title:
						tipo= 'JJ'
						if not(palabra in adjetivos):
							adjetivos.append(palabra)
						pos= 10 if seccion.title.startswith('Adjetivo') else 2
					#Muestra que palabras se han ingresado hasta ahora
					ventana1.Element('muestra').Update('Sustantivos: '+ str(sustantivos) +'\n'+'Verbos: '+str(verbos)+'\n'+'Adjetivos: '+str(adjetivos))
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
					if tipo == 'NN':
						if not(palabra in sustantivos):
							sustantivos.append(palabra)
					elif tipo == 'VB':
						if not(palabra in verbos):
							verbos.append(palabra)
					elif tipo == 'JJ':
						if not(palabra in adjetivos):
							adjetivos.append(palabra)
					ventana1.Element('muestra').Update('Sustantivos: '+ str(sustantivos) +'\n'+'Verbos: '+str(verbos)+'\n'+'Adjetivos: '+str(adjetivos))
					disenio2 =[[sg.Text('La palabra no esta en Wikcionario')],
								[sg.Text('Ingrese una definicion para la palabra '+ palabra), sg.InputText(do_not_clear=False, key= 'definicion')],
								[sg.Button("Agregar")]]
					ventana2= sg.Window('Ingreso de definicion').Layout(disenio2)
					boton, values2= ventana2.Read()
					definicion= values2['definicion']
					dic[tipo][palabra]= definicion
					ventana2.Close()
			else:
				sg.PopupOK('Error 722, Ingrese la palabra otra vez',grab_anywhere=True)
	ventana1.Close()
	return dic
	
def configurar_sopa(diccionario_colores, tipo_ayuda,orientacion_vertical,cant_palabras,sopa_mayusculas,cant_palabras_default,oficina_asignada):
	''' Establece la configuracion de la sopa de letras
	devolviendo los valores ingresados en estructuras de datos.
	En caso de que los colores se repitan se abre una ventana para avisar de esto.
	'''
	import PySimpleGUI as sg
	
	sg.SetOptions(button_element_size=(4, 2), background_color = "grey20")
	# Establece el "look and feel" de la ventana con el promedio de temperatura de las oficinas
	lista_de_oficinas= cambiar_apariencia_ventana()
	
	dic= {'Rojo':'#f54969','Naranja':'#f29741','Plateado':'silver','Amarillo':'#fae050','Verde':'#89eb75','Cyan':'#87ede1','Azul':'#62a2f5','Purpura':'#ae74db','Magenta':'#e36bc5','Rosa':'#fa9ba6'}
	
	elegir_color = [[sg.Text('Elija un color para los sustantivos',background_color = "grey20",text_color = "snow"), sg.InputCombo(['Rojo','Naranja','Plateado','Amarillo','Verde','Cyan','Azul','Purpura','Magenta','Rosa'],default_value='Rojo', key= 'color_sustantivo',background_color = "grey20",text_color = "snow")],
					[sg.Text('Elija un color para los verbos',background_color = "grey20",text_color = "snow"), sg.InputCombo(['Rojo','Naranja','Plateado','Amarillo','Verde','Cyan','Azul','Purpura','Magenta','Rosa'],default_value='Amarillo', key= 'color_verbo',background_color = "grey20",text_color = "snow")],
					[sg.Text('Elija un color para los adjetivos',background_color = "grey20",text_color = "snow"), sg.InputCombo(['Rojo','Naranja','Plateado','Amarillo','Verde','Cyan','Azul','Purpura','Magenta','Rosa'],default_value='Verde', key= 'color_adjetivo',background_color = "grey20",text_color = "snow")]]
	
	elegir_ayuda = [[sg.Checkbox('Mostrar las definiciones de las palabras',key= 'mostrar_def',background_color = "grey20",text_color = "snow")], 
					[sg.Checkbox('Mostrar la lista de palabras a buscar',key= 'mostrar_lista',background_color = "grey20",text_color = "snow")]]
	
	elegir_orientacion = [[sg.Radio('Horizontal', "RADIO1",default=True,key= 'hor',background_color = "grey20",text_color = "snow"), sg.Radio('Vertical', "RADIO1",key= 'vert',background_color = "grey20",text_color = "snow")]]
	
	elegir_cant_palabras = [[sg.Text('Sustantivos',background_color = "grey20",text_color = "snow"), sg.Input(cant_palabras_default[0],key= 'cant_sus',background_color = "grey35",text_color = "snow",size =(3,1))],
							[sg.Text('Verbos      ',background_color = "grey20",text_color = "snow"), sg.Input(cant_palabras_default[1],key= 'cant_ver',background_color = "grey35",text_color = "snow",size =(3,1))],
							[sg.Text('Adjetivos   ',background_color = "grey20",text_color = "snow"), sg.Input(cant_palabras_default[2],key= 'cant_adj',background_color = "grey35",text_color = "snow",size =(3,1))]]
	
	elegir_mayus_minus = [[sg.Radio('Mayuscula', "RADIO2",default=True,key= 'mayus',background_color = "grey20",text_color = "snow"), sg.Radio('Minuscula', "RADIO2",key= 'minus',background_color = "grey20",text_color = "snow")]]
	
	elegir_oficina = [[sg.Text('Elija una oficina para tomar sus datos',background_color = "grey20",text_color = "snow"), sg.InputCombo(lista_de_oficinas,default_value='oficina1', key= 'office',background_color = "grey20",text_color = "snow")]]
		
	configuracion= [[sg.Frame('Colores', elegir_color, background_color = "grey20",title_color = "snow")],
					[sg.T(" ", background_color = "grey20" )],
					[sg.Frame('Tipo de ayuda', elegir_ayuda, background_color = "grey20",title_color = "snow")],
					[sg.T(" ", background_color = "grey20" )],
					[sg.Frame('Orientacion de las palabras', elegir_orientacion, background_color = "grey20",title_color = "snow")],
					[sg.T(" ", background_color = "grey20" )],
					[sg.Frame('Cantidad a mostrar', elegir_cant_palabras, background_color = "grey20",title_color = "snow")],
					[sg.T(" ", background_color = "grey20" )],
					[sg.Frame('Tipo de letra de la sopa de letras', elegir_mayus_minus, background_color = "grey20",title_color = "snow")],
					[sg.T(" ",background_color = "grey20")],
					[sg.Frame('Oficinas', elegir_oficina, background_color = "grey20",title_color = "snow")],
					[sg.T(" "*25,background_color = "grey20"), sg.Button("Listo",size =(10,2) , button_color = ("#ffffff","#3698A9"))]]
					
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
	oficina_asignada.append(values["office"])
