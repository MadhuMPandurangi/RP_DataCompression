import csv

def createCSV():
     with open('./CSV/compression_stats.csv', 'w', newline='') as file:
          writer = csv.writer(file)
          writer.writerow(["File_size","Level","Avg_memory_usage", "Avg_CPU_usage", "Compression_speed","compression_ratio"])

if __name__ == "__main__":
     createCSV()