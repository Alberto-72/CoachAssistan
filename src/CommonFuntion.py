# Here will be all the funtions tha could be reused in all the project

import os
import csv
from time import strftime
def clear_screen():
    """Clears the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu(options):
    """Prints the menu with the given options"""
    clear_screen()
    print("--- Menu ---")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

def ReadFile(filename:str) -> list: # In this project, we just will use csv files
    """Reads a CSV file and returns its data as a list of dicts"""
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

def WriteFile(filename: str, fieldnames:list ,data: dict): # In this project, we just will use csv files
    """Writes data to a CSV file"""
    with open(filename, 'w', newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # Write header row if file is empty
        writer.writerows(data)

def ValidateData (typ, data):
    match typ:
        case "date":
            try:
                strftime(data, "%d/%m/%Y")
                return True
            except:
                return False