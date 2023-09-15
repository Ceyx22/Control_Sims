import matplotlib.pyplot as plt
import csv

def create_fig(xaxis, yaxis, figNum, yaxisName, xaxisName, saveName, case='basic', y2axis=None):
    if case == 'basic':
        plt.figure(figNum)
        plt.plot(xaxis, yaxis)
        plt.xlabel(xaxisName)
        plt.ylabel(yaxisName)
        plt.savefig(saveName)
    elif case == "passive walker":
        plt.figure(figNum)
        plt.plot(xaxis, yaxis, label="Leg 1 Angle", color='blue', linestyle='dashed')
        plt.plot(xaxis, y2axis, label="Leg 2 Angle", color='red', linestyle='dashdot')
        plt.legend()
        plt.xlabel(xaxisName)
        plt.ylabel(yaxisName)
        plt.savefig(saveName)
    else:
        print("Num plots not valid")

def to_CSV(name, unformatted_data, header):
    with open(name, 'w', newline='') as file:
        # Step 4: Using csv.writer to write the list to the CSV file
        writer = csv.writer(file)
        writer.writerow(header)
        for item in unformatted_data:
            writer.writerow(item) # Use writerow for single list