# Here will be all the funtions tha could be reused in all the project

import os
import csv
from time import strptime
def ClearScreen():
    """Clears the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def SelectOption(prompt:str, options:list) -> str:
    """Displays a numbered list of options and returns the selected value."""
    print(prompt)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    while True:
        try:
            op = int(input("Opción: ")) - 1
            if 0 <= op < len(options):
                return options[op]
            else:
                print("Opción inválida. Inténtalo de nuevo.")
        except ValueError:
            print("Entrada no válida. Inténtalo de nuevo.")

def ReadFile(filename:str) -> list: # In this project, we just will use csv files
    """Reads a CSV file and returns its data as a list of dicts"""
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

def WriteFile(filename: str, fieldnames:list ,data: list): # In this project, we just will use csv files
    """Writes data to a CSV file, the data has to  be a list of dicctionaries"""
    with open(filename, 'w', newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # Write header row if file is empty
        writer.writerows(data)

def AppendData(filename: str, fieldnames:list ,data: list):
    """Append data to a CSV file, the data has to be a list of dicctionaries"""
    read_data = ReadFile(filename)
    if not read_data: # Check if in the file there are not any information
        WriteFile(filename, fieldnames, data)
    else:
        with open(filename, 'a', newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerows(data)

def UpdateData(filename: str, fieldnames:list ,data: list, ID_to_Mod:str): 
    """Here will read the file data and when it find the data will be written
    If the data is not found, send None"""

    file_data = ReadFile(filename)
    for row in file_data:
        if row[ID_to_Mod] == data[0][ID_to_Mod]:
            row.update(data[0])
            break
    WriteFile(filename, fieldnames, data)

def ValidateData (typ, data):
    match typ:
        case "date":
            try:
                strptime(data, "%d/%m/%Y")
                return True
            except:
                return False