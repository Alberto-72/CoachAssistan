# In this file will be all the functions related to the players
import src.CommonFuntion as cf
from random import randint
from ast import literal_eval

Player_Data_Filename = "files/Data/PlayerData.csv"
Player_Data_Fieldnames = ["ID_Player", "number", "name", "surname", "birthday", "position", "ID_Team"]

User_Data_Filename = "files/Data/UserData.csv"
User_Data_Fieldnames = ["UserName", "password", "rol", "key"]

# The ID_Player field is made of the first 3 letters of the name + 2 first letters of the surname + sequential number

class Player ():
    def __init__(self, ID_Player: str, number: int, name: str, surname: str, birthday: str, position: str, ID_Team: list):
        self.ID_Player = ID_Player
        self.number = number  # Must be unique and between 1 and 99
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.position = position
        self.ID_Team = literal_eval(ID_Team) if isinstance(ID_Team, str) else ID_Team

    def AddTeam(self, ID_Team):
        """Adds a team to the player, a player could play in a more of 1 team, so it will be a list"""
        
        self.ID_Team.append(ID_Team)
        cf.UpdateData(Player_Data_Filename, Player_Data_Fieldnames, [vars(self)], "ID_Player")
    def __str__(self):
        return f"Nombre: {self.name} {self.surname}, Posición: {self.position}"

def GenerateIDPlayer(name: str, surname: str) -> str:
    """Generates a unique player ID based on name and surname"""
    base_ID = (name[:3] + surname[:2]).upper()
    players = cf.ReadFile(Player_Data_Filename)
    count = sum(1 for player in players if player["ID_Player"].startswith(base_ID))
    return f"{base_ID}{count}"

def Encrypt(password: str) -> tuple:
    """Encrypts a password with a random key shift"""
    key = randint(1, 100)
    alphabet = "áéíóúabcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ ,.;:!?'-_+()}{[]<=>|/\\~123456789"
    encrypted = "".join(alphabet[(alphabet.find(c) + key) % len(alphabet)] if c in alphabet else c for c in password)
    return encrypted, key

def CreatePlayer():
    """Creates a new player and registers them in the system"""

    cf.ClearScreen()
    print("--- REGISTRO DE JUGADOR ---")
    # Personal data of the player
    print("Datos del jugador")
    name = input("Nombre/s: ").strip().title()
    surname = input("Apellidos: ").strip().title()

    while True:
        birthdate = input("Fecha de nacimiento (dd/mm/yyyy): ").strip()
        if cf.ValidateData("date", birthdate): break
        print("Error: Fecha incorrecta")
    
    # Selects the number
    while True:
        number = input("Número 00-99: ").strip()
        if number.isdigit() and 0 <= int(number) <= 99: break
        print("Error: Número incorrecto")
    
    # Selects the position
    position = cf.SelectOption(
        "Seleccione la posición del jugador",
        ["Base", "Escolta", "Alero", "Ala-Pivot", "Pivot"]
    )
    
    ID_Player = GenerateIDPlayer(name, surname)
    New_Player = Player(ID_Player=ID_Player, number=number, name=name, surname=surname, birthday=birthdate, position=position, ID_Team=[])

    # Save player data
    new_player_dict = [{
        "ID_Player": ID_Player,
        "number": number,
        "name": name,
        "surname": surname,
        "birthday": birthdate,
        "position": position,
        "ID_Team": []
    }]
    cf.AppendData(Player_Data_Filename, Player_Data_Fieldnames, new_player_dict)

    # Assign default encrypted password
    password, key = Encrypt("123456")
    new_user_dict = [{
        "UserName": ID_Player,
        "password": password,
        "rol":"player",
        "key": key
    }]
    cf.AppendData(User_Data_Filename, User_Data_Fieldnames, new_user_dict)
    print("Jugador y usuario creado correctamente")
    input("Presione enter para continuar...")

def EditPlayer():
    pass

def DeletePlayer():
    pass

def SelectPlayer():
    """ Select the players of the new team """
    while True:
        cf.ClearScreen()
        print("-- SELECCIONA JUGADORES --")
        players = cf.ReadFile(Player_Data_Filename)
        if not players:
            print("No hay jugadores disponibles. Creando un nuevo jugador.")
            CreatePlayer()
            continue

        Name_Surname = input("Ingrese \"Apellido1 Apellido2, Nombre/s\" del jugador (o enter para terminar): ")
        if not Name_Surname: return None
        if "," not in Name_Surname: 
            print("Formato de introduccion incorrecta, por favor vuelva a intentarlo")
            input("Presione enter para continuar...")
            continue
        Name_Surname = Name_Surname.split(",")
        Filtered_Players = [p for p in players if p["name"] == Name_Surname[1].strip() and p["surname"] == Name_Surname[0]]

        if not Filtered_Players:
            print("No existe ningún jugador con esa descripción.")
            if input("¿Quiere crear un nuevo jugador? (S/N): ").upper() == "S": CreatePlayer()
            continue

        cf.ClearScreen()
        print("--- SELECCIONA JUGADOR ---")
        Selected_Player = cf.SelectOption("Seleccione un jugador:", [f"{p["ID_Player"]}, {p['number']} - {p['name']} {p['surname']}" for p in Filtered_Players])
        Player_Data = next((p for p in players if p["ID_Player"] == Selected_Player.split(",")[0]), None)
        player = Player(**Player_Data)
        break
    return player

def PlayerMenu():
    pass

if __name__ == "__main__": SelectPlayer()