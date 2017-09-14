#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import matplotlib
#ignore all backend Xwindows
#must be imported  directly after matplotlib!
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math


class getData():

	def __init__(self):

		self.data_list = []		#list to store csv data
		self.end = 0
	
	def runWeatherstation(self):

		get_list = []	#Liste aller Werte der csv-Datei
		timeList = []	#list for measuring time
		tempList = []	#list for temperature 
		presList = []	#list for pressure
		humList = []	#list for humidity

		#store csv data
		with open('wetterdaten.csv', 'r') as csvfile:
				data = csv.reader(csvfile, delimiter=',', quotechar=',' )
				get_list.extend(data)

					
		#only take the last ten
		lastTen = len(get_list)-11

		#slicing List to get only the last ten items
		self.data_list = get_list[lastTen:]

		#end of list
		self.end = len(self.data_list)

		#######################################
		##########Preparation for Graphs#######

		#fill timeList with first column and just use time hh:mm 
		for i in range(self.end-1):
			cutStamp1 = self.data_list[i+1][0][13:15]
			cutStamp2 = self.data_list[i+1][0][16:18]
			cutStamp = cutStamp1 + '.' + cutStamp2
			timeList.append(float(cutStamp))

		endTime = len(timeList)-1

		timeList2 = []
		for i in range(self.end-1):
			timeList2.append(self.data_list[i+1][0][13:18])

		#######################################
		###########Temp Graph##################

		#fill tempList with second column
		for i in range(self.end-1):
			newTemp = float(self.data_list[i+1][1])
			newTemp = round(newTemp,1)
			tempList.append(newTemp)
			#tempList.append(int(self.data_list[i+1][1]))
		
		minTemp = math.ceil(min(tempList))
		minTemp = round(minTemp, 1)
		maxTemp = math.ceil(max(tempList))
		maxTemp = round(maxTemp, 1)

		#plot and save graph
		plt.plot(tempList, color='r', linewidth=2.0)
		plt.xticks(range(len(tempList)), timeList2, size='small', rotation=20)
		plt.ylim(math.floor(min(tempList)), math.ceil(max(tempList)))
		plt.xlabel('Time')
		plt.ylabel('Grad Celsius') 
		plt.title('Temperatur')
		plt.grid(True)
		plt.savefig('img/temp.png', format='png', transparent = True)
		plt.close()		#close plot after saving image
						#if you're not closing everything will get mixed up

		#######################################
		#############Pressure- Graph ############

		#fill presList with third column
		for i in range(self.end-1):
			presList.append(float(self.data_list[i+1][2]))
		
		minPres = math.ceil(min(presList))
		minPres = round(minPres, 1)
		maxPres = math.ceil(max(presList))
		maxPres = round(maxPres, 1)

		plt.plot(presList, color='#006400', linewidth=2.0)
		plt.xticks(range(len(presList)), timeList2, size='small', rotation=20)
		#plt.yticks(range(len(presList)), presList, size='small', rotation=20)
		plt.ylim(math.floor(min(presList)), math.ceil(max(presList)))
		#turning of the offset of the y-axis to show big numbers correctly
		plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
		plt.xlabel('Time')
		plt.ylabel('Hektopascal')
		plt.title('Pressure')
		plt.grid(True)
		plt.savefig('img/pres.png', format='png', transparent = True)
		plt.close()

		##########################################
		##############Humidity-Graph##############

		#fill humList with fourth column
		for i in range(self.end-1):
			humList.append(float(self.data_list[i+1][3]))
		
		minHum = math.ceil(min(humList))
		minHum = round(minHum, 1)
		maxHum = math.ceil(max(humList))
		maxHum = round(maxHum, 1)

		plt.plot(humList, color='b', linewidth=2.0)
		plt.xticks(range(len(humList)), timeList2, size='small', rotation=20)
		plt.ylim((minHum-1), (maxHum+1))
		plt.xlabel('Time')
		plt.ylabel('Prozent')
		plt.title('Humidity')
		plt.grid(True)
		plt.savefig('img/hum.png', format='png', transparent = True)
		plt.close()