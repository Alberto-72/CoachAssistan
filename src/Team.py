# This file will execute all the functions related to the teams
import src.CommonFuntion as cf
import src.Player as P
import src.Clubs as Cl
from src.UserValidation import register
import time
import ast

Club_Data_Filename = "files/Data/ClubData.csv"
Club_Data_Fieldname = ["ID_Club", "court", "staff" ,"teams"]

Team_Data_Filename = "files/Data/TeamData.csv"
Team_Data_Fieldname = ["ID_Team", "season", "club", "category", "staff", "players"]

Player_Data_Filename = "files/Data/PlayerData.csv"
Player_Data_Fieldname = ["ID_Player", "number", "name", "surname", "birthday", "position", "ID_Team"]

User_Data_Filename = "files/Data/UserData.csv"

# The Id_Team field is made of the season + 3 first letters of Club + 3 first letters of Category

class Team ():
    def __init__(self, ID_Team: str, Season: str, Club: str, Category: str, Staff: list, Players: list):
        self.Id_Team = ID_Team
        self.Season = Season
        self.Club = Club
        self.Category = Category
        self.Staff = Staff
        self.Players = Players
    
    def __str__(self):
        return f"ID_Team: {self.Id_Team} - {self.Season} - {self.Club} - {self.Category} - {self.Staff} - {self.Players}"

def CreateTeam():
    """Create a new team and save it to the database."""
    cf.ClearScreen()
    print("CREA TU EQUIPO")
    # Select the club of the team
    club = Cl.SelectClub()

    # Select the category of the team
    categories = [
        "Escuelita U6", "Prebenjamin U7", "Benjamin U9", "PreMinibasket U10",
        "Minibasket U11", "PreInfantil U12", "Infantil U13", "PreCadete U14",
        "Cadete U15", "Junior U16-U17", "Senior"
    ]
    category = cf.SelectOption("Seleccione una categoría:", categories)

    # Select the staff of the new team
    Staff_Roles = [
        "HeadCoach - 1er Entrenador", "Assistant Coach - 2o Entrenador",
        "Conditioning Manager - Preparador Físico", "Team Manager - Delegado"
    ]
    Team_Staff = {}
    print("Registra al staff del equipo: ")
    users = cf.ReadFile(User_Data_Filename)
    for role in Staff_Roles:
        while True:
            usr_name = input(f"Ingrese el nombre de usuario del {role} (Presione enter si no tiene ese rol en su equipo): ")
            if not usr_name: break
            # Check if the user already exists
            user = next((u for u in users if u["UserName"] == usr_name), None)
            if not user: 
                ops = ["Volver a intentar", "Registrar nuevo usuario"]
                op = cf.SelectOption(f"No existe el usuario {usr_name}",ops)
                if op == ops[0]: continue
                else: 
                    register()
                    continue
            Team_Staff[role] = usr_name
            break

    # Select the players of the new team
    team_players = []
    while len(team_players) < 16:
        player = P.SelectPlayer()
        if not player: break
        team_players.append(player)

    # Calculates the rest of the necessary information
    season = str(time.localtime().tm_year)
    season = str(int(season[2:]) - 1) + "/" + season[2:]
    ID_Team = f"{season}{club.ID_Club[:3].upper()}{category[:3].upper()}"
    
    # Saves the team to the database and updates the club data
    team_data = [{
        "ID_Team": ID_Team, "season": season, "club": club.ID_Club,
        "category": category, "staff": Team_Staff, "players": [ID.ID_Player for ID in team_players]
    }]
    cf.AppendData(Team_Data_Filename, Team_Data_Fieldname, team_data)

    # Updates the club data to include the new team ID
    club.AddTeam(ID_Team)
    cf.UpdateData(Club_Data_Filename, Club_Data_Fieldname, [vars(club)], ID_to_Mod="ID_Club")
    
    # Updates the player
    for player in team_players:
        player.AddTeam(ID_Team)
        cf.UpdateData(Player_Data_Filename, Player_Data_Fieldname, [vars(player)], ID_to_Mod="ID_Player")

def SelectTeam(User):
    """Allows a user to select a team they belong to."""
    while True:
        teams = cf.ReadFile(Team_Data_Filename)
        Users_Team = [t for t in teams if User.username in ast.literal_eval(t["staff"]).values()]

        if not Users_Team: # If ther are no user's teams
            print("No tienes equipos asignados.")
            if input("¿Quieres crear un equipo? (S/N): ").upper() == "S":
                CreateTeam()
                continue
            return None

        # Generate the lists of all the teams and include the option of creatig another
        options = [f"{t['club']} - {t['category']}" for t in Users_Team]
        options.append("Crear un equipo")
        selected_team = cf.SelectOption("Seleccione uno de sus equipos:", options)

        if not selected_team: # If the user didn't select a team
            print("No se ha seleccionado ningun equipo")
            return None
        if selected_team == "Crear un equipo":
            CreateTeam()
            continue

        # In case the user selected a team, divide the option to catch the ID
        selected_team = selected_team.split("-")
        selected_team = next((t for t in teams if t['club'] == selected_team[0].strip() and t['category'] == selected_team[1].strip()), None)
        return Team(**selected_team)