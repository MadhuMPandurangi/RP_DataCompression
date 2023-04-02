import os
import psutil
import threading
import time
import sys
import matplotlib.pyplot as plt
import calculate_metrics
import subprocess
import re
from CSV import create_csv

flag = 1
cpu_usage_list = []
memory_percent_usage_list = []
compression_time = 0
rkbps_list = []
wkbps_list = []
dkbps_list = []
util_list = []

def compress():
	global flag,compression_time
	start_time = time.time()
	print(sys.argv[1])
	os.system(sys.argv[1])
	final_time = time.time()
	compression_time = round(final_time - start_time,2)
	flag = 0
	
def monitor():
	global flag,cpu_usage_list, rkbps_list, wkbps_list, dkbps_list, util_list
	while(flag):
		x = psutil.cpu_percent(0.5)
		cpu_usage_list.append(x)
		y = psutil.virtual_memory()[2]
		memory_percent_usage_list.append(y)
		output = subprocess.check_output(["sar", "-d", "1", "1"])
		output = output.decode("utf-8")
		lines = output.split("\n")
		for line in lines:
			if re.search("^Average.*dev8.*", line):
				fields = line.split()
				rkbps = fields[3]
				wkbps = fields[4]
				dkbps = fields[5]
				util = fields[9]
				rkbps_list.append(float(rkbps))
				wkbps_list.append(float(wkbps))
				dkbps_list.append(float(dkbps))
				util_list.append(float(util))

def pad_values():
	global cpu_usage_list,memory_percent_usage_list
	start_time = time.time()
	while(time.time() - start_time <= 1.0):
		x = psutil.cpu_percent(0.5)
		y = psutil.virtual_memory()[2]
		cpu_usage_list.append(x)
		memory_percent_usage_list.append(y)
	
	
if __name__ == "__main__":
	
	t1 = threading.Thread(target=compress,name="t1")
	t2 = threading.Thread(target=monitor,name="t2")
	
	#pad_values()
	
	t2.start()
	t1.start()
	
	t2.join()
	t1.join()

	x = sys.argv[1].split()
	org_file_size = os.stat('./{}'.format(x[6]))
	size = org_file_size.st_size
	sizeToStr = str(size)
	plotsPath = './plots/'+sizeToStr
	if not os.path.exists(plotsPath):
		os.makedirs(plotsPath)
	
	#pad_values()
	
	l = len(cpu_usage_list)
	time_values = []
	for i in range(l):
		time_values.append(f"{(i)*0.5}-{(i+1)*0.5}")
	
	plt.bar(time_values, cpu_usage_list)
	plt.xlabel("Time interval")
	plt.ylabel("CPU usage in percentage")
	plt.title("CPU usage for " + sys.argv[2] + ', ' + sys.argv[3])
	plt.tick_params(axis='x', labelrotation=-45)
	plt.figtext(0.7,0.8,"Time taken : " + str(compression_time))
	plt.savefig('./'+plotsPath+'/CPU usage for ' + sys.argv[2] + '.png')
	plt.close()
	
	plt.bar(time_values, memory_percent_usage_list)
	plt.xlabel("Time interval")
	plt.ylabel("Memory usage in percentage")
	plt.title("Memory usage for " + sys.argv[2]+ ', ' + sys.argv[3])
	plt.tick_params(axis='x', labelrotation=-45)
	plt.figtext(0.7,0.8,"Time taken : " + str(compression_time))
	plt.savefig('./'+plotsPath+'/Memory usage for ' + sys.argv[2] + '.png')
	plt.close()
	

	path = './CSV/compression_stats.csv'
	isExist = os.path.isfile(path)
	if(not(isExist)):
		create_csv.createCSV()
	x = sys.argv[1].split()
	if(x[3][2].isnumeric()):
		level = int(x[3][1])*10 + int(x[3][2])	
		calculate_metrics.computeMetrics(level,x[5], x[6], compression_time,cpu_usage_list,memory_percent_usage_list, rkbps_list, wkbps_list, dkbps_list, util_list)
	else:
		if(x[3][1].isnumeric()):
			calculate_metrics.computeMetrics(x[3][1],x[5], x[6], compression_time,cpu_usage_list,memory_percent_usage_list, rkbps_list, wkbps_list, dkbps_list, util_list)
		elif(x[4][1].isnumeric()):
			level = int(x[4][1])*10 + int(x[4][2])
			calculate_metrics.computeMetrics(level,x[6], x[7], compression_time,cpu_usage_list,memory_percent_usage_list, rkbps_list, wkbps_list, dkbps_list, util_list)
	
		

