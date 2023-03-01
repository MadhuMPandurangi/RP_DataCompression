import os
import matplotlib.pyplot as plt
import statistics

# Set the path to the folder containing the files
path = "DataSet/github"

# Initialize variables for file sizes and serial numbers
sizes = []
serial_numbers = []

# Traverse the folder and get the sizes and serial numbers of all files
for i, filename in enumerate(os.listdir(path)):
    filepath = os.path.join(path, filename)
    if os.path.isfile(filepath):
        size = os.path.getsize(filepath)
        sizes.append(size)
        serial_numbers.append(i)

# Calculate median and mean file sizes
median_size = statistics.median(sizes)
mean_size = statistics.mean(sizes)

# Create the histogram plot
plt.hist(sizes, bins=20)
plt.xlabel('File Size')
plt.ylabel('Frequency')
plt.title('Histogram of File Sizes')
plt.text(20, max(plt.ylim())/2, f'Median File Size: {median_size}\nMean File')
#plt.text(100, max(plt.ylim())/2, f'Mean File Size: {mean_size}\nMean File')
plt.show()