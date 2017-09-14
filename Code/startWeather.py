#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, run, template, static_file
import wetterstation as weatherdata
import web
import threading
import datetime
import time
import os


#route for application
@route('/weather')
def weather():
	 return template('weather', temp = newData.data_list[newData.end-1][1], pres = newData.data_list[newData.end-1][2], hum = newData.data_list[newData.end-1][3])

#static route for generated graphs
@route('/img/<filename>')
def send_static(filename):
	return static_file(filename, root='./img/')

def runSite():
	#test
	#run(host='localhost', port=8080)
	#run @ pi
	run(host='0.0.0.0', port=8080)

def sensorData():
	while (True):
		time.sleep(5)
		weatherdata.Write_Data()

def webData():
	while (True):
		time.sleep(5)
		newData.runWeatherstation()
	


if __name__ == '__main__':	
	print("Initializing...")
	print("To close this programme press STRG+C two times")
	print("Once to shut down the server and once to end the programme")

	for i in range(10):
		weatherdata.Write_Data()

	newData = web.getData()
	newData.runWeatherstation()
	
	#######################
	threadData = threading.Thread(target=webData)
	threadSensor = threading.Thread(target=sensorData)
	########

	threadRun = Thread(runSite())
	threadRun.start()
	
	threadData.start()
	threadSensor.start()
	
	try:
		while (True):
			pass
	except KeyboardInterrupt:
		print('keyboardinterrupt')
		#kills all python processes
		os.system("sudo kill `ps -a | grep python | awk '{print $1}'`")
