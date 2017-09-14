# Basis einer minimalen Wetterstation
# I2C mittels Bitbanging, da der MLP3115A2 ein Repeated-Startbit benoetigt
#
# Autor: Kai-Uwe Mrkor
# Datum: 25.11.2013
#


import RPi.GPIO as GPIO
import os
import csv
import time
import datetime


# Adressen der I2C-Bausteine
MPL3115A2 = 0xC0  # Drucksensor MPL3115A2
TMP102 = 0x90     # Temperatursensor TMP102
HIH6130 = 0x4E    # Feuchtesensor HIH 6130

# Definition von Konstanten fuer das Bit R/W
WRITE = 0
READ  = 1

# I2C-Pins vereinbaren
SDA = 2 # GPIO 02 bzw. Pin 3
SCL = 3 # GPIO 03 bzw. Pin 5

# Acknowledge und None Acknowledge festlegen
ACK = 0
NACK = 1

#
# Initialisierung der verwendeten Portpins
#
def I2C_Init():

	# Warnungen unterdruecken
	GPIO.setwarnings(False)

	# nachfolgend immer die GPIO-Nummern verwenden
	GPIO.setmode(GPIO.BCM)

	# Beide als Ausgang (inkl. Pullup-Widerstand) konfigurieren
	GPIO.setup(SDA, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(SCL, GPIO.OUT, pull_up_down=GPIO.PUD_UP)

	# Beide geben H aus
	GPIO.output(SDA, GPIO.HIGH)
	GPIO.output(SCL, GPIO.HIGH)

	return


#
# Startbit senden    
#
def I2C_Start():	
	
	# Uebergang von 1 auf 0 auf SDA
	GPIO.output(SDA, GPIO.LOW)
	GPIO.output(SCL, GPIO.LOW)

	return


#
# Startbit vor einem Empfang erneut senden
#
def I2C_RepeatStart():	

	# Vorbereiten
	GPIO.output(SDA, GPIO.HIGH)
	GPIO.output(SCL, GPIO.HIGH)
	
	# Uebergang von 1 auf 0 auf SDA
	GPIO.output(SDA, GPIO.LOW)
	GPIO.output(SCL, GPIO.LOW)

	return	


#
# Stoppbit senden
#
def I2C_Stop():	

	# Uebergang von 0 auf 1 auf SDA
	GPIO.output(SDA, GPIO.LOW)		
	GPIO.output(SCL, GPIO.HIGH)		
	GPIO.output(SDA, GPIO.HIGH)
	
	return


#
# Bitweises Empfangen eines Bytes
# (mit MSB beginnend)	
#
def I2C_Read_Byte( ack):	

	eingelesen = 0
	GPIO.setup(SDA, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	eingelesen_str = ""

	for i in range(8):

		eingelesen <<= 1
		
		# Bit einlesen und einreihen
		GPIO.output(SCL, GPIO.HIGH)

		#time.sleep(0.01)

		if (GPIO.input(SDA) == 1):
			eingelesen +=1
			eingelesen_str += '1'			
		else:
			eingelesen_str += '0'			
		
		# Pegelwechsel am Takt-Pin zur Uebernahme
		GPIO.output(SCL, GPIO.LOW)
		
	# SDA wieder auf Ausgang
	GPIO.setup(SDA, GPIO.OUT, pull_up_down=GPIO.PUD_UP)

        #time.sleep(0.05)

	# Acknowledge 
	if (ack == NACK):
		GPIO.output(SDA, GPIO.HIGH)
	else:
		GPIO.output(SDA, GPIO.LOW)
		GPIO.output(SCL, GPIO.HIGH)	
		GPIO.output(SCL, GPIO.LOW)        

	#print eingelesen_str 	
		
	return eingelesen


#	
# Bitweises Senden eines Bytes
# (mit MSB beginnend)	
#
def I2C_Write_Byte( ausgabe):	

	ausgabe_str = ""

	for i in range(8):
		
		# Bit ausgeben
		if (ausgabe & 0x80):
			GPIO.output(SDA, GPIO.HIGH)
			ausgabe_str += '1'			
		else:
			GPIO.output(SDA, GPIO.LOW)
			ausgabe_str += '0'			
		
		# Pegelwechsel am Takt-Pin zur Uebernahme
		GPIO.output(SCL, GPIO.HIGH)
		GPIO.output(SCL, GPIO.LOW)
		
		# naechstes Bit
		ausgabe <<= 1

	# SDA auf Einlesen
	GPIO.setup(SDA, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	# Takt fuer Acknowledge 	
	GPIO.output(SCL, GPIO.HIGH)
	if (GPIO.input(SDA) == 1):
		print "Kein ACK vom Sensor !!!"	
	GPIO.output(SCL, GPIO.LOW)

	#SDA wieder auf Ausgabe
	GPIO.setup(SDA, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
	GPIO.output(SDA, GPIO.LOW)

	#print ausgabe_str 	
		
	return

	

#
# Datum in ein Register des MPL schreiben
#	
def Write_Reg_MPL( reg, wert):

	I2C_Start()
	I2C_Write_Byte( MPL3115A2 + WRITE)	# Bausteinadresse  + Schreibsignal
	I2C_Write_Byte( reg)			# Adresse des Registers
	I2C_Write_Byte( wert)
	I2C_Stop()

	return


#
# Datum aus einem Register des MPL lesen
#	
def Read_Reg_MPL( reg):

	I2C_Start()
	I2C_Write_Byte( MPL3115A2 + WRITE)	# Bausteinadresse  + Schreibsignal
	I2C_Write_Byte( reg)			# Adresse des Registers

	# Repeated START	
	I2C_RepeatStart()

	I2C_Write_Byte( MPL3115A2 + READ)	# Bausteinadresse  + Lesesignal
	eingelesen = I2C_Read_Byte( ACK)
	I2C_Stop()

	return eingelesen


#
# Datum aus einem Register des TMP102 lesen
#	
def Read_TMP102( ):

	# Zeigerregister des TMP102 auf 0x00 setzen
	I2C_Start()
	I2C_Write_Byte( TMP102 + WRITE)  # Bausteinadresse  + Schreibsignal
	I2C_Write_Byte( 0x00)   	 # Adresse des Registers
	I2C_Stop()
        
	# Vorher ausgewaehltes Register auslesen
	I2C_Start()
	I2C_Write_Byte( TMP102 + READ)   # Bausteinadresse  + Lesesignal
	eingelesen_h = I2C_Read_Byte( ACK)
	eingelesen_l = I2C_Read_Byte( ACK)
	I2C_Stop()

	#print eingelesen_h, eingelesen_l

	temp = (eingelesen_h << 4) | (eingelesen_l >> 4)

	# Zweierkomplement ausgleichen
	if (eingelesen_h & 0x80):
		temp |= (-1 - 0xFF)

	#print hex(eingelesen_h), hex(eingelesen_l), hex(temp)

	return temp * 0.0625



#
# HIH6130 auslesen
#	
def Read_HIH6130( ):

	# Messung starten
	I2C_Start()
	I2C_Write_Byte( HIH6130 + WRITE)        # Bausteinadresse  + Schreibsignal
	I2C_Stop()

	# Messung braucht mind. 38 ms
	time.sleep(0.05)

	# Feuchte und Temperatur auslesen
	I2C_Start()
	I2C_Write_Byte( HIH6130 + READ)	        # Bausteinadresse  + Lesesignal                
	feuchte_h = I2C_Read_Byte(ACK)
	feuchte_l = I2C_Read_Byte(ACK)
	temp_h = I2C_Read_Byte(ACK)
	temp_l = I2C_Read_Byte(NACK)
	I2C_Stop()


#        print feuchte_h, feuchte_l, temp_h, temp_l

#       status = feuchte_h >> 6
#       print "\nStatus",status,"\n"

	feuchte = ((feuchte_h & 0x3F) << 8 ) | feuchte_l
	temp = (temp_h << 6) | ((temp_l & 0xFC) >> 2)


#        print hex(feuchte), hex(temp), "\n"

	feuchte = (feuchte * 100) / 16383.0
	temp = ( (temp*165) / 16383.0 ) - 40.0

	#print feuchte, "--", temp

	return feuchte, temp



#
# MPL auslesen
#	
def Read_MLP( ):
	# whoami-Register des MLP auslesen 
	#print "Who am i = ", hex(Read_Reg_MPL( 0x0C)), "\n\n"		
	if (Read_Reg_MPL( 0x0C) != 0xC4):
		print "WhoAmI-Register konnte nicht ausgelesen werden"

	########################################################

	# Datenflags setzen
	Write_Reg_MPL( 0x13, 0x07)

	# Einzelmessung des Hoehenmessers starten
	Write_Reg_MPL( 0x26, 0x82)

	# Auf Ende der Messung warten
	nochmal = 1
	while nochmal:
		time.sleep(0.1)
		status = Read_Reg_MPL( 0x00) 		
		if (status & 0x08):
			nochmal = 0

	# Hoehe auslesen
	hoehe_h = Read_Reg_MPL( 0x01) 		
	hoehe_m = Read_Reg_MPL( 0x02) 		
	hoehe_l = Read_Reg_MPL( 0x03) 		

	# Temperatur auslesen
	temp_h = Read_Reg_MPL( 0x04) 		
	temp_l = Read_Reg_MPL( 0x05)

	########################################################

	# Datenflags setzen
	Write_Reg_MPL( 0x13, 0x07)

	# Einzelmessung des Barometers starten
	Write_Reg_MPL( 0x26, 0x02)

	# Auf Ende der Messung warten
	nochmal = 1
	while nochmal:
		time.sleep(0.1)
		status = Read_Reg_MPL( 0x00) 		
		if (status & 0x08):
			nochmal = 0

	# Druck auslesen
	druck_h = Read_Reg_MPL( 0x01) 		
	druck_m = Read_Reg_MPL( 0x02) 		
	druck_l = Read_Reg_MPL( 0x03) 		

	# Temperatur auslesen
	temp_h = Read_Reg_MPL( 0x04) 		
	temp_l = Read_Reg_MPL( 0x05)

	########################################################

	#### Temperatur berechnen ####
	if (temp_h & 0x80):
		temp = ~(0xFF - temp_h) + 1
		temp += (temp_l >> 4)/16.0
	else:
		temp = temp_h
		temp += (temp_l >> 4)/16.0

	#### Hoehe bestimmen ####
	if (hoehe_h & 0x80):
		hoehe =  -((~( (hoehe_h << 8) | hoehe_m) + 1) & 0xFFFF)
		hoehe -= (hoehe_l >> 4)/16.0
	else:
		hoehe = (hoehe_h << 8) | hoehe_m
		hoehe += (hoehe_l >> 4)/16.0
       

	#### Druck bestimmen ####
	druck = (druck_h << 10) | (druck_m << 2) | (druck_l >> 6)
	druck += ((druck_l >> 4) & 0x03)/4.0
	druck /= 100

	return druck, hoehe, temp


########################################################
#CSV-Datei anlegen und Daten rein schreiben
def Write_Data():

	I2C_Init()

	# Log-Datei einrichten
	if os.path.exists("wetterdaten.csv"):
		with open("wetterdaten.csv","r+") as csvfile:
			datawriter = csv.writer( csvfile, quotechar=',', quoting =csv.QUOTE_MINIMAL)
			datawriter.writerow( ["Zeitstempel","Temp(C)","Luftdruck(hPa)","Luftfeuchte(%)"])
	else:
		with open("wetterdaten.csv","w") as csvfile:
			datawriter = csv.writer( csvfile, quotechar=',', quoting =csv.QUOTE_MINIMAL)
			datawriter.writerow( ["Zeitstempel","Temp(C)","Luftdruck(hPa)","Luftfeuchte(%)"])
	
	#while True:

		#print "MLP\n---"
	mlp_druck, mlp_hoehe, mlp_temp = Read_MLP()
		#print round(mlp_hoehe,1),"m"
		#print round(mlp_druck,1),"hPa"
		#print round(mlp_temp,1),"C"


	tmp102_temp = Read_TMP102()
		#print  "\nTMP102\n------"
		#print round(tmp102_temp,1), "C"


		#print  "\nHIH6130\n-------"
	hih_feuchte, hih_temp = Read_HIH6130()
		#print round(hih_feuchte,1), "% Luftfeuchtigkeit"
		#print round(hih_temp,1), "C"

		#print "\n====================================\n"


		# aktuelle Daten im Log ablegen
	with open("wetterdaten.csv","a+") as csvfile:
		datawriter = csv.writer( csvfile, quotechar=',', quoting =csv.QUOTE_MINIMAL)
		t = datetime.datetime.now()
		zeitstempel = t.strftime("%d.%m.%Y - %H:%M:%S")
		datawriter.writerow( [zeitstempel,round(tmp102_temp,1),round(mlp_druck,1),round(hih_feuchte,1)])

