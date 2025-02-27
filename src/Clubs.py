import src.CommonFuntion as cf
from ast import literal_eval

class Club:
    """This class represents a club."""
    def __init__(self, ID_Club:str, court:list = [], teams:list = [], staff:list = []):
        self.ID_Club = ID_Club
        self.court = literal_eval(court) if isinstance(court, str) else court
        self.teams = literal_eval(teams) if isinstance(teams, str) else teams
        self.staff = literal_eval(staff) if isinstance(staff, str) else staff
    
    # Modify the court attribute
    def AddCourt(self, court):
        self.court.append(court)
    
    def RemoveCourt(self, court):
        if court in self.court:
            literal_eval(self.court).remove(court)

    # Modify and Show the team attribute
    def AddTeam(self, ID_Team): 
        self.teams.append(ID_Team)

    def RemoveTeam(self, ID_Team):
        if ID_Team in self.teams:
            literal_eval(self.teams).remove(ID_Team)

    def SearchTeam(self, ID_Team):
        return any(ID_Team == t["ID_Team"] for t in self.teams)
    
    # Modify and show the staff attribute
    def AddStaff(self, ID_Staff):
        literal_eval(self.staff).append(ID_Staff)

    def RemoveStaff(self, ID_Staff):
        if ID_Staff in self.staff:
            literal_eval(self.staff).remove(ID_Staff)

    def SearchStaff(self, ID_Staff):
        return any(ID_Staff == s["ID_Staff"] for s in self.staff)
    
    def __str__(self):
        return f"Club: {self.ID_Club}, Cancha: {', '.join(self.court)}"

Club_Data_Filename = "files/Data/ClubData.csv"
Club_Data_Fieldname = ["ID_Club", "court", "staff" ,"teams"]

def CreateClub():
    """Create a new club and save it to the database."""
    name = input("Ingrese el nombre del club: ").upper()
    court = []

    while True:
        Name_Court = input("Ingrese el nombre de la cancha (presione enter cuando no hayan más): ").upper()
        if not Name_Court:
            break
        court.append(Name_Court)

    New_Club = {"ID_Club": name, "court": court, "staff":[] ,"teams": []}
    cf.AppendData(Club_Data_Filename, Club_Data_Fieldname, [New_Club])

def SelectClub() -> Club:
    """ Select the club of the new team """
    cf.ClearScreen()
    while True:
        clubs = cf.ReadFile(Club_Data_Filename)
        if not clubs:
            op = input("No hay clubes disponibles. Quiere crear un nuevo club? (S/N) ")
            if op.upper() == "N": return
            CreateClub()
            continue
        options = [c["ID_Club"] for c in clubs]
        options.append("Crear otro club")
        club = cf.SelectOption("Seleccione un club:", options)
        if club.upper() == "CREAR OTRO CLUB": 
            CreateClub() # In case of the user wanna create a new club
            continue
        Club_Data = next((c for c in clubs if c["ID_Club"] == club), None)
        club = Club(**Club_Data)
        break
    return club

