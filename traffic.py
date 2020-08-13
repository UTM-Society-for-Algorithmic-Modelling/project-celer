import csv
import matplotlib.pyplot as plt
import networkx as nx


def process_traffic(path):
    """
    Process the given clean Traffic Data file.
    Returns dictionary of street names, with list of traffic volume throughout a 24HR period. 

    Duplicate keys are merged and corresponding values averaged according to time.

    Parameters: (path)
    path - string
    """
    return extract_data(path)


def extract_data(path):
    """
    ******Reads manually formatted files**********
    Given clean CSV in format: Roadway Name, Traffic Data per hour (24 HR TIME, 24 HRS)
    Returns a dictionary in the format: {'Roadway_Name': ['Traffic Figures from 0-23 HR']}
    
    Duplicate keys, value pairs are merged and averaged.

    Parameters: (path)
    path - string
    """
    traffic = {}
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            row[0] = row[0].upper()
            if (row[0]) not in traffic:
                traffic[row[0]] = row[1:]
            else:
                old_list = traffic[row[0]]
                new_values = row[1:]
                traffic[row[0]] = merge_lists(old_list, new_values)

    del traffic['ROADWAY NAME']
    return traffic


def merge_lists(old_list, new_list):
    """
    Returns an averaged list of traffic values in a 24HR window, given two lists. 

    Parameters: (old_list, new_list)
    old_list = list
    new_list = list    
    """
    final = []
    for i in range(24):
        if not old_list[i]:
            old_list[i] = 0
        if not new_list[i]:
            new_list[i] = 0

        x = (int(old_list[i]) + int(new_list[i]))
        final.append(x // 2)

    return final


def clean_data(path):
    """
    OPTIONAL - format dependent.
    ****Formats file into multiline CSV, currently not being used******
    Using: NYC Traffic Volume Count 2014-2018
    Takes "traffic_volume.csv" and returns simplified, formatted 'edited_traffic_volume.csv' file (in same directory). Deletes all extra columns except: {Roadway Name, Times}  

    Parameters: (path)
    path - string
    """

    with open(path, "rt") as csvfile, open("edited_traffic_volume.csv", "wt") as csvout:
        reader = csv.reader(csvfile, delimiter="\n")
        writer = csv.writer(csvout, delimiter="\n")
        rows = list(reader)
        for line in rows:
            output = line[0].split(',')
            processed_line = output[2:3] + output[7:]
            writer.writerow(processed_line)
