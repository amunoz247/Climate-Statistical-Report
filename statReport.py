# /usr/bin/env python3

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#   Climate Statiscal Report Program
#
#   Authors: Andrew Munoz
#   Date: 06/01/2021
#   Purpose: Perform simple data analysis on elevation values found in CSV data files.
#   Input: Takes in two command line arguments - CSV file data and a US State two-letter abbreviation
#   Output: Outputs a statistical report in a JSON-file format containing number of stations and max, min, median, and average values. 
#
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import os
import sys
import csv
import json

# Main function to run the program
def main():

    # Command Line Input Values
    dataFile = input("Enter the data file you would like to process: ")
    state = input("Enter the two-letter abbreviation for the state you are looking for: ")
    # dataFile = sys.argv[1]
    # state = sys.argv[2]

    # Error Handling for incorrect input values
    try:
        with open(dataFile, 'r') as inputFile:
            inputFile.read()
    except FileNotFoundError:
        print("\nFileNotFoundError: The file '%s' does not exist. Please select a different data file to process." % dataFile)
        sys.exit()
    # Check abbreviation length for state string and if string is lowercase
    if len(state) > 2:
        print("\nValueError: Input '%s' is incorrect for State Abbreviation. State Abbreviation should be two letters." % state)
        sys.exit()
    if state.islower():
        state = state.upper()

    # Create an output JSON file path
    jsonOutputFile = r'Output/elevation_report_%s.json' % state

    # Print Information to Command Line
    print("\nFile Selected: ", dataFile)
    print("State Selected: ", state)

    # Call function to read CSV file and create JSON output report
    statReport(dataFile, state, jsonOutputFile)

    print("Stat report output file is saved as: ", jsonOutputFile)

# Function to read/process CSV and create JSON statistical report
# Takes in the csv file, state, and json file path as parameters
def statReport(csvFilename, stateAbbreviation, jsonFilename):
     
    # Create a list for data values found in csv
    data = []

    # Create lists for cleaned data and stations missing data
    stateArray = []
    elevMissing = []

    # Initialize additional variables
    elevationMax = {"elev" : -99999.0}
    elevationMin = {"elev" : 99999.0}
    elevationMedian = 0
    elevationAverage = 0
    elevSum = 0
    numStationsTotal = 0
    numStationsWD = 0

    # Initialize Json Output Array
    jsonArray = {}
    jsonArray['header'] = []
    jsonArray['max'] = []
    jsonArray['min'] = []
    jsonArray['median_elev'] = []
    jsonArray['average_elev'] = []
     
    # Read csv file with DictReader
    with open(csvFilename) as csvf:
        csvReader = csv.DictReader(csvf)
        # Loop through rows in csv and add data to dictionary list
        for row in csvReader:
            data.append(row)

    # Loop through dictionary list
    for row in range(len(data)):    
        # Look for state abbreviation passed in through command line
        # Create list of state stations and count number of stations
        if data[row]["state"] == stateAbbreviation:
            numStationsTotal += 1
            if data[row]["elev"] == "":
                elevMissing.append(data[row])
                continue
            data[row]["elev"] = float(data[row]["elev"])
            stateArray.append(data[row])
            numStationsWD += 1
    # Sort Station list by elevation value
    stateArray = sorted(stateArray, key = lambda i: i['elev'])

    # Check if abbreviation is not found in the dataset
    if numStationsTotal == 0:
        print("\nState '%s' not found in the dataset." % stateAbbreviation)
        print("Exiting Program...")
        sys.exit()

    # Loop through clean data set
    for row in stateArray:
        # Look for elevation stat values (max, min, and sum)
        if float(row["elev"])  >= float(elevationMax["elev"]):
            elevationMax = row
        if float(row["elev"])  <= float(elevationMin["elev"]):
            elevationMin = row
        elevSum += float(row["elev"])
    
    # Calculate elevation average
    elevationAverage = elevSum / numStationsWD
    
    # Calculate elevation median
    mid = len(stateArray) // 2
    elevationMedian = (stateArray[mid]["elev"] + stateArray[~mid]["elev"]) / 2

    # Format Header for Json output file
    jsonArray['header'].append({
    'State' : stateAbbreviation,
    'Total Number of Stations': numStationsTotal,
    'Number of Stations with Elevation Data': numStationsWD
})

    # Add Stat Values to the Json output file
    jsonArray['max'].append(elevationMax)
    jsonArray['min'].append(elevationMin)
    jsonArray['median_elev'].append(elevationMedian)
    jsonArray['average_elev'].append(round(elevationAverage, 2))
 
    # Open the Json file and write to file using the json.write() and json.dumps() functions
    with open(jsonFilename, 'w') as jsonf:
        jsonf.write(json.dumps(jsonArray, indent=4))

# Run Program
if __name__ == "__main__":
    main()