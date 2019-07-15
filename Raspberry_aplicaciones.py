#Alumnos:
# Motocanchi Huanca, Elvis David
# D'Aragona Agustin Alejandro

from Raspberry_Clases import Temperatura
from Raspberry_Clases import Matriz
import json

def registro_ambiental(archivos):
	''' Recibe una lista con los nombres de las oficinas
	y actualiza el archivo de temperaturas y humedad
	'''
	temp_hum= Temperatura()
	datos= temp_hum.datos_sensor()
	arch= open('Json_files/datos-oficinas.json', 'r')
	dic_temp_hum= json.load(arch)
	if type(dic_temp_hum) != dict:
		dic_temp_hum= {}
	arch.close()
	#actualiza la oficina1 que seria el unico modificado por el sensor
	dic_temp_hum['oficina1'].append(datos)
	arch= open('Json_files/oficina1.json', 'w')
	json.dump(dic_temp_hum,arch)
	arch.close()
	if archivos != []:
		#actualiza la info contando a los demas archivos oficina en caso de que estos existan y fueran modificados
		for i in archivos:
			oficina= open('Json_files/'+i+'.json', 'r')
			info= json.load(oficina)
			if i in dic_temp_hum.keys():
				if info != {}:
					dic_temp_hum[i].append(info)
			else:
				if info != {}:
					dic_temp_hum[i]= [info]
			oficina.close()
	arch= open('Json_files/datos-oficinas.json', 'w')
	json.dump(dic_temp_hum,arch)
	arch.close()

def muestra_datos(datos):
	''' Muestra la temperatura y humedad promedio de
	la oficina seleccionada en las matrices de leds
	'''
	led= Matriz()
	led.mostrar_mensaje(str('Temperatura 'datos[0])+' '+ 'Humedad '+str(datos[1]), 0.1, 1)
