import psutil
import subprocess
import matplotlib.pyplot as plt
import os
import sys

def plot_graph(file_path):
    cpu_usage = []
    memory_usage = []
    disk_io = []
    x_axis = range(1, 23)

    for level in range(1, 23):
        p = subprocess.Popen(['time', '-f%U:%M:%S', 'gzip', '-'+str(level), file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        process_info = psutil.Process(p.pid)
        cpu_usage.append(process_info.cpu_percent())
        memory_usage.append(process_info.memory_info().rss)
        disk_io.append(process_info.io_counters().read_bytes + process_info.io_counters().write_bytes)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
    fig.suptitle(f'Performance Analysis of {file_path}')
    ax1.bar(x_axis, cpu_usage, width=0.5, align='center')
    ax1.set_title('CPU Usage')
    ax1.set_xlabel('z standard level')
    ax1.set_ylabel('Usage (%)')
    ax2.bar(x_axis, memory_usage, width=0.5, align='center')
    ax2.set_title('Memory Usage')
    ax2.set_xlabel('z standard level')
    ax2.set_ylabel('Usage (Bytes)')
    ax3.bar(x_axis, disk_io, width=0.5, align='center')
    ax3.set_title('Disk I/O Data')
    ax3.set_xlabel('z standard level')
    ax3.set_ylabel('Data (Bytes)')
    plt.savefig(f'{file_path}_performance.png')

if __name__ == '__main__':
    x = sys.argv[1].split()
    org_file_size = os.stat('./{}'.format(x[6]))
    size = org_file_size.st_size	
    sizeToStr = str(size)
    plotsPath = './plots/'+sizeToStr
    file_paths = ['./'+plotsPath+'/Memory usage for 1', './'+plotsPath+'/Memory usage for 2', './'+plotsPath+'/Memory usage for 3']
    for file_path in file_paths:
        plot_graph(file_path)
