import os
import os
from statistics import mean
from csv import writer
from CSV import create_csv


def computeMetrics(level,zipFileName, fileName, tot_comp_time, cpu_usage_list, memory_percent_usage_list, rkbps_list, wkbps_list, dkbps_list, util_list):
	zip_file_size = os.stat('./{}'.format(zipFileName))
	org_file_size = os.stat('./{}'.format(fileName))
	avg_cpu_usage = mean(cpu_usage_list)
	avg_mem_usage = mean(memory_percent_usage_list)
	compressedFileSize = zip_file_size.st_size
	originalFileSize = org_file_size.st_size
	compRatio = compressedFileSize/originalFileSize if (originalFileSize != 0)  else compressedFileSize  
	compSpeed = originalFileSize/tot_comp_time if( tot_comp_time != 0) else originalFileSize
	avg_rkbps = sum(rkbps_list)/len(rkbps_list) if( len(rkbps_list) != 0) else sum(rkbps_list)
	avg_wkbps = sum(wkbps_list)/len(wkbps_list) if( len(wkbps_list) != 0) else sum(wkbps_list)
	avg_dkbps = sum(dkbps_list)/len(dkbps_list) if( len(dkbps_list) != 0) else sum(dkbps_list)
	avg_util = sum(util_list)/len(util_list) if( len(util_list) != 0) else sum(util_list)
	populateCSV(originalFileSize,level,avg_mem_usage, avg_cpu_usage, compSpeed, compRatio, avg_rkbps, avg_wkbps, avg_dkbps, avg_util)
	# print("AVG CPU: ",avg_cpu_usage)
	# print("AVG Memory Usage: ",avg_mem_usage)
	# print("Level of compression: ", level)
	# print("Size of compressed file :", zip_file_size.st_size, "bytes")
	# print("Size of original file :", org_file_size.st_size, "bytes")
	# print("Compression Ratio: ", zip_file_size.st_size/org_file_size.st_size)
	# print("Total compression time: ", tot_comp_time)
	# print("Compression Speed: ", (org_file_size.st_size/tot_comp_time), "Bps")
	# print("-------------------------------------------")

def populateCSV(org_file_size,level,avg_mem_usage, avg_cpu_usage, compSpeed, compRatio, avg_rkbps, avg_wkbps, avg_dkbps, avg_util):
	row = [org_file_size,level,avg_mem_usage, avg_cpu_usage, compSpeed, compRatio, avg_rkbps, avg_wkbps, avg_dkbps, avg_util]
	with open('./CSV/compression_stats.csv', 'a') as csv_object:
		writer_object = writer(csv_object)
		writer_object.writerow(row)
		csv_object.close()