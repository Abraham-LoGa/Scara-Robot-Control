"""
Nombre: López García Abraham
Grado: 7°   Grupo: 5
Dinámica de Robots
   ----------------------------- CONTROL DE ROBOT SCARA-----------------------
"""
  # Importamos Librerías
from tkinter import *
import serial
import time
import cv2
import numpy as np

  # Declaramos variables
L1 = 100
L2=90
Programar_trayectorias=[]

  # Iniciamos Comunicación serial
#s_C=serial.Serial('COM11',baudrate = 9600, timeout = 9 , parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

  # Funciones para crear herramientas
def boton(Name_object,Text,llamar,cord_x,cord_y,w,h):
		botonG=Button(Name_object,text=Text,command=llamar,width=w,height=h)
		botonG.place(x=cord_x,y=cord_y)	
def label_box(Name_object,Text,cord_x,cord_y,tipo_d_Letra,tamano):
	LabelG=Label(Name_object,text=Text)
	LabelG.place(x=cord_x,y=cord_y)
	LabelG.configure(font=(tipo_d_Letra,tamano))

  # Declaramos nuestra ventana y sus características
windows = Tk()
windows.title('SCARA ROBOT')
windows.geometry("800x500")
ef=StringVar()
ef.set("40")

# Función para el cambio de posición por medio de ángulos
def angle (int):
	dz = Z.get()
	a_1=str(T_1.get())
	a_2=str(T_2.get())
	d_z = map(dz,0,12,0,180)
	ang_r=str(d_z)
	e=str(ef.get())
	d_t=str(a_1+","+a_2+","+ang_r+","+e)
	#s_C.write((d_t + '\n').encode())  
  # Funcion para guardar trayectoria
def guardar_t():
	  # Obtenemos valores
	dz = Z.get()
	d_z = map(dz,0,12,0,180)
	t_1 = T_1.get()
	t_2 = T_2.get()
	a =int (ef.get())
	  # Añadimos valores
	Programar_trayectorias.append(t_1)
	Programar_trayectorias.append(t_2)
	Programar_trayectorias.append(d_z)
	Programar_trayectorias.append(a)

	# Mostrar trayectoria
def trayectoria():
	  # Guardamos valores
	P = np.array(Programar_trayectorias).reshape(-1,4)
	  # Ciclo para mostrar posciones
	for i in range(P.shape[0]):
		a_1 = str(int(P[i,0]))
		a_2 = str(int(P[i,1]))
		d_z = str(int(P[i,2]))
		e = str(int(P[i,3]))
		data = str(a_1+","+a_2+","+d_z+","+e)
		  # Enviamos los datos al arduino con un tiempo de 1 seg	
		#s_C.write((data + '\n').encode())
		time.sleep(1)


  # Función para borrar datos almacenados
def limpiar():
	Programar_trayectorias.clear()
  # Función para convertir de cm a ángulos
def map(x,in_min,in_max,out_min,out_max):
	ang = (x-in_min)*(out_max - out_min)/(in_max - in_min) + out_min;
	return ang

  # Función para cerrar el efector
def Close():
	x = Z.get()
	a_1=str(T_1.get())
	a_2=str(T_2.get())
	d_a = map(x,0,12,0,180)
	ang_r=str(int(d_a))
	ef.set('40')
	d_t=str(a_1+","+a_2+","+ang_r+","+str(ef.get()))
	#s_C.write((d_t + '\n').encode())
  
  # Función para cerrar el efector
def Open():
	x =Z.get()
	a=str(60)
	a_1=str(T_1.get())
	a_2=str(T_2.get())
	d_a = map(x,0,12,0,180)
	ang_r=str(int(d_a))
	ef.set('60')
	d_t=str(a_1+","+a_2+","+ang_r+","+str(ef.get()))
	#s_C.write((d_t + '\n').encode())
  
  # Función para parte de la visión artificial
  # Posicionamiento de efector conforme a coordenadas
def cinematica_Inv():
	  # Obtención de datos de coordenadas
	t_r = float(T_2.get())
	x = float(C_X.get())
	y = float(C_Y.get())
	z = float(C_Z.get())

	  # Obtención de ángulos
	if (x<=190 and x>=-190 and y <=190 and y >= -90 and z<=90 and z >= 0 ):
		Theta2 = (np.arccos((x**2 + y**2 - L1**2 - L2**2)/(2 * L1 * L2)))*180/np.pi
		Theta2aux = np.arccos((x**2 + y**2 - L1**2 - L2**2)/(2 * L1 * L2))
		if (t_r >90):
			Theta2 = np.round(Theta2 + 90)
		else:
			Theta2 = np.round((Theta2 - 90))
		T_2.set(Theta2)
		Theta1 = (np.arctan2(x,y)- np.arctan2((L2*np.sin(Theta2aux)),(L1+L2*np.cos(Theta2))))*180/np.pi
		if (t_r > 90):
			Theta1 = np.round(- (Theta1 - 90) - (t_r - 90)*0.8468201937)
		else:
			Theta1 = np.round(- (Theta1 - 90))
		T_1.set(Theta1)
		Z.set(z)
def vision():
	cap = cv2.VideoCapture(2,cv2.CAP_DSHOW)
	#Declaramos las matrices de colores
	azulBajo = np.array([110,100,30],np.uint8)
	azulAlto = np.array([120,255,255],np.uint8)
	amarilloBajo = np.array([15,100,20],np.uint8)
	amarilloAlto = np.array([40,255,255],np.uint8)
	redBajo1 = np.array([0,100,20],np.uint8)
	redAlto1 = np.array([3,255,255],np.uint8)
	redBajo2 = np.array([177,100,20],np.uint8)
	redAlto2 = np.array([179,255,255],np.uint8)
	font = cv2.FONT_HERSHEY_SIMPLEX

	#Definimos la funcion para la elaboracion de contornos
	def dibujar(mask,color):
		contornos, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		for c in contornos:
			area = cv2.contourArea(c)
			if area > 4000:
				x,y,w,h = cv2.boundingRect(c)
				if color == (255,0,0):
					cv2.rectangle(frame,(x,y),(x+w,y+h),color,3)
					cv2.putText(frame,'Azul',(x-10,y-10), font, 0.75,color,2,cv2.LINE_AA)
	                  # Posiciones conforme al detectar un color
					d_t=str(str(90)+","+str(90)+","+str(10)+","+str(60))
					#s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(d_a)+","+str(60))
	                #s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(d_a)+","+str(40))
	                #s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(10)+","+str(40))
	                #s_C.write((d_t + '\n').encode())
					time.sleep(1)
	                  # Posiciones a la posición de descargue
					d_a = map(12,0,12,0,180)
					d_t=str(str(40)+","+str(90)+","+str(10)+","+str(40))
					#s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(40)+","+str(90)+","+str(10)+","+str(60))
	                #s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(0,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(10)+","+str(60))
					#s_C.write((d_t + '\n').encode())
					time.sleep(1)
				if color == (0,255,255):
					cv2.rectangle(frame,(x,y),(x+w,y+h),color,3)
					cv2.putText(frame,'Amarillo',(x-10,y-10), font, 0.75,color,2,cv2.LINE_AA)
					d_a = map(0,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(0)+","+str(60))
	                #s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(d_a)+","+str(60))
	                #s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(d_a)+","+str(40))
	                #s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(0)+","+str(40))
	                #s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(40)+","+str(43)+","+str(0)+","+str(40))
	                #s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(40)+","+str(43)+","+str(0)+","+str(60))
	                #s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(0,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(0)+","+str(60))
	                #s_C.write((d_t + '\n').encode())
					time.sleep(1)
					
				if color == (0,0,255):
					cv2.rectangle(frame,(x,y),(x+w,y+h),color,3)
					cv2.putText(frame,'Rojo',(x-10,y-10), font,0.75,color,2,cv2.LINE_AA)
					d_a = map(0,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(10)+","+str(60))
					#s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(d_a)+","+str(60))
					#s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(d_a)+","+str(40))
					#s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(10)+","+str(40))
					#s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(50)+","+str(110)+","+str(10)+","+str(40))
					#s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(12,0,12,0,180)
					d_t=str(str(50)+","+str(110)+","+str(10)+","+str(60))
					#s_C.write((d_t + '\n').encode())
					time.sleep(1)
					d_a = map(0,0,12,0,180)
					d_t=str(str(90)+","+str(90)+","+str(10)+","+str(60))
					#s_C.write((d_t + '\n').encode())
					time.sleep(1)
					dato=ser.write(bytearray("r","ascii"))
					#ser.write(bytearray("c","ascii"))
	#Inicia el ciclo
	while True:
		ret,frame = cap.read()
		if ret == True:
			frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
			maskAzul = cv2.inRange(frameHSV,azulBajo,azulAlto)
			maskAmarillo = cv2.inRange(frameHSV,amarilloBajo,amarilloAlto)
			maskRed1 = cv2.inRange(frameHSV,redBajo1,redAlto1)
			maskRed2 = cv2.inRange(frameHSV,redBajo2,redAlto2)
			maskRed = cv2.add(maskRed1,maskRed2)
	         # Casa
			dibujar(maskAzul,(255,0,0))
			dibujar(maskAmarillo,(0,255,255))
			dibujar(maskRed,(0,0,255))
			#cv2.imshow('frame',frame)
			if cv2.waitKey(1) & 0xFF == ord('s'):
				break
	#Destruimos ventanas
	cap.release()
	cv2.destroyAllWindows()



  # Título 
L_0=label_box(windows,"         CONTROL DE ROBOT SCARA       ",130,20,"Arial",20)
  # Angulos
L_0=label_box(windows,"Posicion con angulos ",160,75,"Arial",12)
L_X=label_box(windows," Angulo 1 :",25,115,"Calibri",14)
T_1=Scale(windows, from_= 0, to= 180, orient= HORIZONTAL, command=angle,length=250)
T_1.pack()
T_1.place(x=120,y=100)
T_1.set(90)
L_Y=label_box(windows," Angulo 2 :",25,165,"Calibri",14)
T_2=Scale(windows, from_= 0, to= 180, orient= HORIZONTAL, command=angle,length=250)
T_2.pack()
T_2.place(x=120,y=150)
T_2.set(90)
L_Z=label_box(windows," Z :", 50,215,"Calibri",14)
Z=Scale(windows, from_= 2, to= 12, orient= HORIZONTAL, command=angle,length=250)
Z.pack()
Z.place(x=120,y=200)
Z.set(5)
L_P=label_box(windows," Pinzas", 200,260,"Calibri",14)
B_E0=boton(windows,"CERRAR",Close,140,300,10,1)
B_E1=boton(windows,"ABRIR",Open,250,300,10,1)
  # Coordenadas
L_0=label_box(windows,"Posicion por coordenadas ",530,75,"Arial",12)
L_C_X=label_box(windows,"X",520,118,"Corbel",11)
C_X=Entry(windows)
C_X.place(x=550,y=120)
L_C_Y=label_box(windows,"Y",520,155,"Corbel",11)
C_Y=Entry(windows)
C_Y.place(x=550,y=160)
L_Z=label_box(windows,"Z",520,195,"Corbel",11)
C_Z=Entry(windows)
C_Z.place(x=550,y=200)
B_M=boton(windows,"Mover",cinematica_Inv,560,250,13,1)

  # Programación de Trayectorias
L_0=label_box(windows,"Programar posiciones ",160,370,"Arial",12)
B_G=boton(windows,"Guardar",guardar_t,60,420,13,1)
B_M=boton(windows,"Mover",trayectoria,180,420,13,1)
B_L=boton(windows,"Limpiar Trayectoria",limpiar,300,420,15,1)

  # Boton de visión artificial
L_0=label_box(windows," Vision Artificial",560,370,"Arial",12)

B_E1=boton(windows,"VISION",vision,560,420,13,1)

  # INICIO DE NUESTRA VENTANA
windows.mainloop()
