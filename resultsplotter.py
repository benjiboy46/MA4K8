import matplotlib.pyplot as plt
import csv

file_path = 'array_of_results_FJ.csv' #change based on what results
file_path2 = 'array_of_results_FJBA.csv'

# Initialize empty lists to store the X and Y data
x_data = []
y_data = []
x_data2 = []
y_data2 = []

# Read data from the CSV file
with open(file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:

        x_data.append(float(row[0]))
        y_data.append(float(row[1]))

with open(file_path2, mode='r') as file2:
    csv_reader2 = csv.reader(file2)
    for row in csv_reader2:

        x_data2.append(float(row[0]))
        y_data2.append(float(row[1]))

# Plotting the data
plt.plot(x_data, y_data, marker='o', label = 'W-S', color = 'blue')  
plt.plot(x_data2, y_data2, marker='o', label = 'B-A', color = 'red')  
plt.xlabel('Number of Media Nodes',fontsize = 16)  
plt.ylabel('Number of Happy Agents', fontsize = 16) 
plt.legend(fontsize = 13)
plt.savefig('resultsFJ.png') #chnage based on model used
plt.close()