import pandas as pd
import matplotlib.pyplot as plt
import os

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('/home/kannan/Desktop/DATA COMPRESSION/RP_DataCompression/CSV/compression_stats.csv')
mypath = ('/home/kannan/Desktop/DATA COMPRESSION/RP_DataCompression/plots/summary')

# Loop through each file size and each column and create a bar graph
for file_size in df['File_size'].unique():
    df_filtered = df[df['File_size'] == file_size]
    for col in df.columns[1:]:
        plt.figure()
        for i in range(1, 23):
            df_level = df_filtered[df_filtered['Level'] == i]
            plt.bar(i, df_level[col], label='Level ' + str(i))
        
        plt.xlabel('Compression Level')
        plt.ylabel(col)
        plt.title('File Size: ' + str(file_size))
        plt.legend()
        plt.savefig(os.path.join(mypath, f'{col}_{file_size}.png'))
        plt.show()
