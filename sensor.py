import csv
import os
from ina219 import INA219
from ina219 import DeviceRangeError
from time import sleep
from datetime import datetime


now = datetime.now()
print(now)
current_time = now.strftime("%d_M%m_%Y-%H_m%M") #obtener fecha y hora para nombre de archivo

file_name = f'data_{current_time}.csv' #nombre de archivo segun hora


# Función para limpiar pantalla
def clear():
	os.system("clear")

# Parámetros de sensor

i= -10  # numero decimales
SHUNT = 0.1
max_AMP = 1.0
add = 0x40
ina = INA219(SHUNT,max_AMP,address=add)
ina.configure(ina.RANGE_16V)

#diccionario con datos
rec_data = {"time":now,
		"voltage":0,
		"current":0,
		"shunt_v":0}

# creo archivo de datos
with open(file_name, 'w', newline='') as f:

    writer = csv.writer(f)
    writer.writerow(rec_data.keys())


# Actualizar archivo de datos
def file_update(rec_data):
	with open(file_name, 'a', newline='') as f2:
		writer2 = csv.writer(f2)
		writer2.writerow(rec_data.values())


def read():


	try:
		current = "%.5f" % ina.current()

		voltage = "%.5f" % ina.voltage()
		shunt_volt = "%.5f" % ina.shunt_voltage()
		hora = datetime.now().strftime("%H:%M:%S.%f")[0:-3]

		rec_data["time"] = hora
		rec_data["voltage"] = voltage
		rec_data["current"] = current
		rec_data["shunt_v"] = shunt_volt
		file_update(rec_data)
		print(f"Hora: {hora}")
		print(f"Bus Voltage: {voltage} V")
		print(f"Bus Current: {current} mA")
		print(f"Shunt voltage: {shunt_volt} mV")



	except DeviceRangeError as e:
		# Current out of device range with specified shunt resistor
		print(e)
	sleep(0.5)

if __name__ == "__main__":
	while True:
		read()
		clear()
