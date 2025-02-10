# In this file will be all the funcions related to the players

import CommonFuntion as cf

Player_Data_filename = "files/Data/PlayerData.csv"
Player_Data_fieldnames = ["ID_Player", "Number", "Name", "Surname", "Birthday", "Position", "ID_Team"]

User_Data_filename = "files/Data/UserData.csv"

# The ID_Player field is made of the first 3 letter of the name + 2 first letters of the surname + numbers that correspond to the number of useres with the same name

class Player:
    def __init__(self, ID_player: str, number:int, Name: str, Surname: str, Birthday: str, Position: str, ID_team: str):
        self.ID_player = ID_player
        self.Number = number  # It must be unique and between 1 and 99
        self.Name = Name
        self.Surname = Surname
        self.Birthday = Birthday
        self.Position = Position
        self.ID_team = ID_team
    
    def __str__(self):
        return f"Nombre: {self.Name} {self.Surname}, Posición: {self.Position}"

def CreatePlayer():
    def GenerateIDPlayer(name, surname) -> str:
        ID_Player = name[0:3] + surname[0:2]
        i = 0
        Users = cf.ReadFile(User_Data_filename)
        for user in Users:
            if user["UserName"] == name.startswith(ID_Player):
                i+=1
        return ID_Player + str(i)
    print ("Datos del jugadaor")
    name = input("Nombre/s: ")
    surname = input("Apellidos: ")
    
    while True:
        number = input("Numero 00-99: ")
        if number.isdigit() or 00 >= int(number) <= 99: break
        else: print ("Error: Número incorrecto")
    
    while True:
        birthdate = input("Fecha de nacimiento (dd/mm/yyyy): ")
        if cf.ValidateData("date", birthdate): break
        else: print ("Error: Fecha incorrecta")
    
    while True:
        position = int(input("Posición con numero (1 - Base, 2 - Escolta...): "))
        if 1 <= position <= 5: break
        print ("Error: Posición incorrecta")
    ID_Player = GenerateIDPlayer(name, surname)
    ID_Team = ""
    New_Player = Player(ID_Player, number, name, surname, birthdate, position, ID_Team)
def EditPlayer():
    pass

def DeletePlayer():
    pass

def PlayerMenu():
    pass