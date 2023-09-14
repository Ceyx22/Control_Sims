import matplotlib.pyplot as plt
import csv

def create_fig(xaxis, yaxis, figNum, yaxisName, xaxisName, saveName):
    plt.figure(figNum)
    plt.plot(xaxis, yaxis)
    plt.xlabel(xaxisName)
    plt.ylabel(yaxisName)
    plt.savefig(saveName)

def to_CSV(name, unformatted_data, header):
    with open(name, 'w', newline='') as file:
        # Step 4: Using csv.writer to write the list to the CSV file
        writer = csv.writer(file)
        writer.writerow(header)
        for item in unformatted_data:
            writer.writerow(item) # Use writerow for single list