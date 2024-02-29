import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

min_voltage = 600
max_voltage = 780
excluded_voltages = []
minutes = 7
vbias = 29.5

mins_in_milliseconds = minutes * 60 * 1000

expected_muons = 25 * 5 * minutes #Expected muon number. Area is 25cm x 5cm, expect 1 muon per cm^2 per min, seven mins

#Set current directory
current_directory = os.getcwd()

#Get a list of all the items inside of the directory
entries = os.listdir(current_directory)

#Add entries to a list of files if the entry is a file!
files = [f for f in entries if os.path.isfile(os.path.join(current_directory,f))]

files_sanitised = [] #Contains only the voltages numbers on the file
files_csv = []

#Find all .csv files and append to list. Also strip the A.csv from each.
for file in files:
    if '.csv' in file:
        df = pd.read_csv(file)
        count = df[' count0 ']
        #Make sure that there is more than one time entry!
        if len(count) > 1:
            file_stripped = ''.join(letter for letter in file if letter.isdigit())
            
            if float(file_stripped) >= min_voltage and float(file_stripped) <= max_voltage and float(file_stripped) not in excluded_voltages:
                files_csv.append(file)
                files_sanitised.append(file_stripped)

voltages = [] #Stores value of threshold voltages

#Count values for each of the coincidences
counts_0 = []
counts_1 = []
counts_2 = []
counts_3 = []
counts_4 = []
counts_5 = []



#Add the numerical value from the sanitised list to the voltages array
for i in files_sanitised:
    voltages.append(float(i))


#Extracting data from each of the files. See photo for coincidence setup

for file in files_csv:
    df = pd.read_csv(file)
    time = df[' time ']

    #Different coincidence count rates
    count0 = df[' count0 ']
    count1 = df[' count1 ']
    count2 = df[' count2 ']
    count3 = df[' count3 ']
    count4 = df[' count4 ']
    count5 = df[' count5 ']

    i = 1
    ready = False

    while not ready:
        #Scan through the values in the time column until the total interval is 7 minutes
        dt = time[i] - time[0]

        if abs(dt - mins_in_milliseconds) <= 10000:
            ready = True
        elif i + 1 == len(time) and abs(dt - mins_in_milliseconds) > 10000:
            raise ValueError(f'Fewer than {minutes} minutes recorded in {file}')
        else:
            #Increase index by 1
            i = i + 1

    counts_0.append((count0[i]-count0[0]))
    counts_1.append((count1[i]-count1[0]))
    counts_2.append((count2[i]-count2[0]))
    counts_3.append((count3[i]-count3[0]))
    counts_4.append((count4[i]-count4[0]))
    counts_5.append((count5[i]-count5[0]))

expected = np.full_like(voltages, expected_muons, dtype=float)

plt.plot(voltages, expected, label='Expected count')
plt.plot(voltages, counts_0, label='A&&B&&C&&D')
plt.plot(voltages, counts_1, label='(A||B)&&(C||D)')
plt.plot(voltages, counts_2, label = '(A&&B)||(C&&D)')
plt.plot(voltages, counts_3, label='Any single SiPM')
plt.plot(voltages, counts_4, label = 'Any two SiPMs')
plt.plot(voltages, counts_5, label = 'Any Three SiPMS')
plt.yscale('log')
plt.xlabel('Threshold Voltages / mV')
plt.ylabel('Counts over 7 minutes')
plt.title(f'Observed Coincidence Counts over {minutes} min, Vbias = {vbias}V')
plt.legend()
plt.savefig('coincidence_test_1')
plt.show()


    