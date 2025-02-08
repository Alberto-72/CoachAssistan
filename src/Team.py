# This file will execute all the functions related to the teams
import src.CommonFuntion as cf
import src.Player as P
import time

Team_Data_Filename = "files/Data/TeamData.csv"
Team_Data_Fieldname = ["Id_Team", "Season", "Club", "Category", "Staff", "Players"]

Club_Data_Filename = "files/Data/ClubData.csv"
Club_Data_Fieldname = ["Name", "Court", "Teams"]

Player_Data_Filename = "files/Data/PlayerData.csv"

# The Id_Team field is made of the season + 3 first letters of Club + 3 first letters of Category

class Team:
    def __init__(self, Id_Team:str, Season:str, Club:str, Category:str, Staff:list, Players:list):
        self.Id_Team = Id_Team
        self.Season = Season
        self.Club = Club
        self.Category = Category
        self.Staff = Staff
        self.Players = Players

def CreateClub():
    name = input("Ingrese el nombre: ").upper()
    court = []
    while True:
        name_court = input ("Ingrese el nombre de la cancha (pulse @ cuando no hayan mas): ")
        if name_court == "@": break
        court.append(name_court.upper())
    new_club = [{"Name":name, "Court":court, "Teams":""}]
    # Corresponde a los equipos del club, que como es de nueva creacion no tiene de momento
    cf.WriteFile(Club_Data_Filename, Club_Data_Fieldname, new_club)
def CreateTeam ():
    for field in Team_Data_Fieldname:
        match field:
            case "Club":
                while True:
                    Clubs = cf.ReadFile(Club_Data_Filename)
                    print("Seleccione un club:")
                    for i, club in enumerate(Clubs):
                        print(f"{i+1}. {club['Name']}")
                    op = input("Añadir un club (S/N): ")
                    if op.upper() == "S": 
                        CreateClub()
                        continue
                    elif not Clubs: return
                    else: 
                        try:
                            op = int(input("Opcion de club: "))
                            if 0 < op > len(Clubs): raise ValueError("ERROR: Opcion no valida")
                            club = Clubs[op-1]
                            break
                        except ValueError as e:
                            print(e)
                            continue
            case "Category":
                Categories = ["Escuelita U6", "Prebenjamin U7", "Benjamin U9", "PreMinibasket U10", 
                            "Minibasket U11", "PreInfantil U12", "Infantil U13", "PreCadete U14", "Cadete U15", "Junior U16-U17", "Senior"]
                print("Seleccione una categoría:")
                for i, category in enumerate(Categories):
                    print(f"{i+1}. {category}")
                while True:
                    try:  
                        op = int(input("Opcion: ")) - 1
                        if op < 0 or op >= len(Categories):
                            raise ValueError("Opción inválida")
                        Category = Categories[op]
                        break
                    except ValueError as e:
                        print(e)
                        continue
            case "Staff":
                Staff = ["HeadCoach - 1er Entrenador", "Assistant Coach - 2o Entrenador", "Conditioning Manager - Preparador Fisico", "Team Manager - Delegado"]
                Team_staff = []
                print("Ingrese el staff Técnico del equipo (Ingrese @ si su equipo no cuenta con alguno de ellos): ")
                for staff in Staff:
                    Team_staff.append(input(f"Nombre del {staff}: "))
            case "Players":
                Players = cf.ReadFile(Player_Data_Filename)
                Team_players = []
                i = 0
                while i < 16:
                    print(f"Jugador {i+1}:")
                    name_surname = input ("Ingrese el \"Apellido1 Apellido2, Nombre/s\" del jugador (Ingrese @ cuando no haya mas jugadores que añadir): ")
                    if name_surname == "@": break
                    name_surname = name_surname.split(",")
                    for player in Players:
                        if player["Name"] == name_surname[1] and player["Surname"] == name_surname[0]:
                            Team_players.append(player)
                            i += 1
                            break
                    else:
                        print("El jugador no existe.")
                        op = input ("Quiere crear un nuevo jugador (S/N): ")
                        if op.upper() == "S":
                            P.CreatePlayer()
            case _: 
                continue
    season = str(time.localtime().tm_year)
    season = str(int(season[2:]) - 1) + "/" + season[2:]
    ID_TEAM = season + club["Name"][0:3] + category[0:3]
    data = {"Id_Team":ID_TEAM, "Season":season, "Club":club, "Category":category, "Staff":staff, "Players":Players}
    cf.WriteFile(Team_Data_Filename, Team_Data_Fieldname, data)
def UpdateTeam ():
    pass

def DeleteTeam ():
    pass

def SelectTeam (User):
    data = cf.ReadFile(Team_Data_Filename)
    print("Seleccione uno de tus equipo:")
    for i, row in enumerate(data):
        if User.rol in row["Staff"]:
            print(f"{i+1}. {row['Club']} - {row['Category']}")
    op = input ("Quiere crear un equipo (S/N): ")
    if op.upper() == "S": CreateTeam()
    elif not data: return
    while True:
        try:
            op = int(input("Seleccione un equipo: ")) - 1
            if op <= 0 or op > len(data):
                raise ValueError("Opción inválida")
            Selected_Team = Team(data[op]["Id_Team"], data[op]["Season"], data[op]["Club"], data[op]["Category"], data[op]["Staff"], data[op]["Player"])
            return Selected_Team
        except ValueError as e:
            print(e)