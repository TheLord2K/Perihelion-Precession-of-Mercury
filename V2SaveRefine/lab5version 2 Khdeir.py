## PERIHELION  Mercury's perihelion precession and general relativity
#
#


#

import numpy as np  
from scipy import stats  
import matplotlib.pyplot as plt  
import csv  

def main():
    # Load, locate, select, refine, make plot, and save data
    data = loaddata('horizons_results')  # Load data from a specified file path
    data = locate(data)  # Filter data based on vector lengths (perihelia)
    data = select(data, 50, ('Jan', 'Feb', 'Mar'))  # Select data based on year step and specified months
    data = refine(data, 'horizons_results')  # Refine data by loading additional information for each entry
    makeplot(data, 'horizons_results')  # Generate and save a plot
    savedata(data, 'horizons_results')  # Save data to a CSV file

 # Convert a line of comma-separated values to a dictionary.
    # Args:
    # - line (str): Input line with comma-separated values.
    # Returns:
    # - dict: Dictionary with 'numdate', 'strdate', and 'coord'.
def str2dict(line):
    line = (line.split(','))  # Split the line into a list of values
    numdate = float(line[0])  # Convert the first value to a float (numdate)
    strdate = line[1].split(' ')[2]  # Extract the third word from the second value (strdate)
    xcoord = float(line[2])  # Convert the third value to a float (xcoord)
    ycoord = float(line[3])  # Convert the fourth value to a float (ycoord)
    zcoord = float(line[4])  # Convert the fifth value to a float (zcoord)
    coord = (xcoord, ycoord, zcoord)  # Create a tuple with x, y, z coordinates
    return {'numdate': numdate, 'strdate': strdate, 'coord': coord}  # Return a dictionary with numdate, strdate, and coord
 # Filter data based on vector lengths.
    # Args:
    # - data1 (list): List of dictionaries containing data.
    # Returns:
    # - list: Filtered data based on vector lengths.
def locate(data1):
    v_length = []  # Initialize an empty list for vector lengths
    for datum in data1:  # Iterate through data1
        coord = np.array(datum['coord'])  # Convert the 'coord' values to a NumPy array
        dot = np.dot(coord, coord)  # Calculate the dot product of the array with itself
        v_length.append(np.sqrt(dot))  # Append the square root of the dot product to the dist list

    data2 = []  # Initialize an empty list for filtered data
    for c in range(1, len(v_length) - 1):  # Iterate through the range of dist
        if v_length[c] < v_length[c - 1] and v_length[c] < v_length[c + 1]:  # Check for local minima in dist
            data2.append(data1[c])  # Append the corresponding data1 entry to data2

    return data2  # Return the filtered data

 # Add a best fit line to the plot.
    # Args:
    # - numdate (list): List of numerical dates.
    # - actual (list): List of actual data.
    # Returns:
    # - None
def add2plot(numdate, actual):
    line_fitting = stats.linregress(numdate, actual)  # Calculate linear regression statistics
    best_line_fit = [line_fitting[0] * x + line_fitting[1] for x in numdate]  # Generate a best fit line based on the regression statistics
    plt.plot(numdate, best_line_fit, 'b-')  # Plot the best fit line on the existing plot
    plt.title("Slope of Best Fit Line" + " " + str(format(line_fitting[0] * 100 * 365.25, '.2f')) + " " + "arcsec/cent")  # Set the plot title with the slope in arcsec/cent

# Calculate precession angles and return relevant data.
    # Args:
    # - data (list): List of dictionaries containing data.
    # Returns:
    # - tuple: Tuple containing lists of 'numdate', 'strdate', and 'arcsec'.
def precess(data):
    numdate = []  # Initialize an empty list for numdate
    strdate = []  # Initialize an empty list for strdate
    arcsec = []  # Initialize an empty list for arcsec
    l = np.array(data[0]['coord'])  # Set the reference vector using the first entry in data
    for datum in data:  # Iterate through data
        z = np.array(datum['coord'])  # Set the perihelion vector for each entry in data
        ratio = np.dot(z, l) / np.sqrt(np.dot(z, z) * np.dot(l, l))  # Calculate the cosine of the angle between u and v
        if np.abs(ratio) <= 1:  # Check if the ratio is within the valid range for arccos
            angle_to_arcsec_conversion = 3600 * np.degrees(np.arccos(ratio))  # Convert the angle to arcseconds and append to arcsec list
            numdate.append(datum['numdate'])  # Append numdate to the numdate list
            strdate.append(datum['strdate'])  # Append strdate to the strdate list
            arcsec.append(angle_to_arcsec_conversion)  # Append the calculated angle to the arcsec list

    return numdate, strdate, arcsec  # Return the calculated data

 # Save data to a CSV file.
    # Args:
    # - data (list): List of dictionaries containing data.
    # - filename (str): File path for saving the CSV file.
    # Returns:
    # - None
def savedata(data, filename):
    horizon_excel_sheet_header = ['NUMDATE', 'STRDATE', 'XCOORD', 'YCOORD', 'ZCOORD']  # Define the header for the CSV file
    with open(filename + '.csv', 'w', newline='', encoding='UTF-8') as f:  # Open the CSV file for writing
        writer = csv.writer(f)  # Create a CSV writer
        writer.writerow(horizon_excel_sheet_header)  # Write the header to the CSV file
        for relevant_item in data:  # Iterate through data
            excel_row = [relevant_item['numdate'], relevant_item['strdate'], relevant_item['coord'][0], relevant_item['coord'][1], relevant_item['coord'][2]]  # Create a row with relevant data
            writer.writerow(excel_row)  # Write the row to the CSV file

# Generate and save a plot based on processed data.
    # Args:
    # - data (list): List of dictionaries containing data.
    # - filename (str): File path for saving the plot.
    # Returns:
    # - None
def makeplot(data, filename):
    numdate, strdate, arcsec = precess(data)  # Calculate precession angles and obtain relevant data
    plt.plot(numdate, arcsec, 'bo')  # Plot precession angles against perihelion dates
    plt.xticks(numdate, strdate, rotation=45)  # Set x-axis ticks with perihelion dates and rotate them for better visibility
    add2plot(numdate, arcsec)  # Add a best fit line to the plot
    plt.savefig(filename + '.png', bbox_inches='tight')  # Save the plot as a PNG file
    plt.ylabel("Precession (arcsec)")  # Set y-axis label
    plt.xlabel("Perihelion date")  # Set x-axis label
    plt.legend(["Actual Data", "Best Fit Line"])  # Add a legend to the plot
    plt.show()  # Display the plot

# Select data based on year step and specified months.
    # Args:
    # - data (list): List of dictionaries containing data.
    # - ystep (int): Year step for selection.
    # - month (tuple): Tuple of specified months.
    # Returns:
    # - list: Selected data based on criteria.
def select(data, ystep, month):
    selected_data = []  # Initialize an empty list for selected data
    for index in data:  # Iterate through data
        year, m, day = index['strdate'].split('-')  # Split the 'strdate' into year, month, and day
        if int(year) % ystep == 0 and m in month:  # Check if the year is divisible by ystep and the month is in the specified list
            selected_data.append(index)  # Append the index to the selectlist

    return selected_data  # Return the selected data

# Refine function to load additional data for each entry and select the first entry.
    # Args:
    # - data (list): List of dictionaries containing data.
    # - filename (str): File path for loading additional data.
    # Returns:
    # - list: Refined data.
def refine(data, filename):
    newdata = []  # Initialize an empty list for refined data
    for item in data:  # Iterate through data
        ref_filename = filename + '_' + item['strdate']  # Create a new filename based on the existing filename and perihelion date
        refdata = loaddata(ref_filename)  # Load additional data
        refdata = locate(refdata)  # Filter additional data based on vector lengths
        newdata += [refdata[0]]  # Add the first entry of the refined data to the newdata list
    return newdata

 # Load data from a file, process it, and perform necessary operations.
    # Args:
    # - filepath (str): File path for loading data.
    # Returns:
    # - list: Processed data.
def loaddata(filename):
    with open(filename + '.txt', 'r') as file:  # Open the file for reading
        lines = file.readlines()  # Read all lines from the file

    no_presence_of_SOE = True  # Initialize a flag for the presence of $$SOE line
    num_counter = 0  # Initialize a counter for the number of lines
    data = []  # Initialize an empty list for data

    for line in lines:  # Iterate through lines
        if no_presence_of_SOE:
            if line.rstrip() == "$$SOE":  # Check for the $$SOE line
                no_presence_of_SOE = False  # Set the flag to False when $$SOE is found
        elif line.rstrip() != "$$EOE":  # Check for the $$EOE line
            num_counter = num_counter + 1  # Increment the line counter
            if num_counter % 10000 == 0:  # Print progress every 10000 lines
                print(filename, ":", num_counter, "line(s)")
            datum = str2dict(line)  # Convert the line to a dictionary
            data.append(datum)  # Append the dictionary to the data list
        else:
            break  # Exit the loop when $$EOE is found

    if no_presence_of_SOE:
        print(filename, ": no $$SOE line")  # Print a warning if $$SOE line is not found
    else:
        print(filename, ":", num_counter, "line(s)")  # Print the total number of lines

    return data  # Return the loaded data


main()
