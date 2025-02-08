# COACH ASSISTANT

# IDEAS DE INCORPORACIONES
# Leer partidos del pdf de la federacion y que los incluya en mi calendario

import src.CommonFuntion as cf
import src.UserValidation as uv
import src.Team as T
from src.Practices import PracticesMenu
from src.Player import PlayerMenu
from src.Games import GamesMenu
def Main():
    cf.clear_screen()
    print("--- COACH ASSISTANT ---")
    print("1. Iniciar sesión")
    print("2. Registrar")
    print("3. Salir")

    option = input("Elija una opción: ")

    if option == "1":
        user = uv.login()
        MainMenu(user)
    elif option == "2":
        uv.register()
    elif option == "3":
        print("Adiós!")
    else:
        print("Opción inválida. Intente de nuevo.")
        MainMenu()

def MainMenu(user):
    if user.rol == "Coach":
        while True:
            print (f"Bienvenido {user.username} como Coach!")
            Team = T.SelectTeam(user)
            if not Team: continue
            print ("MENU PRINCIPAL")
            print ("1. MENU ENTRENOS")
            print ("2. MENU JUGADORES")
            print ("3. MENU PARTIDOS")
            print ("4. SALIR")
            op = input("Opcion: ")
            match op:
                case "1": PracticesMenu()
                case "2": PlayerMenu(Team)
                case "3": GamesMenu(Team)
                case "4":
                    print("Saliendo...")
                    break
                case _:
                    print("Opción inválida. Intente de nuevo.")
if __name__ == '__main__':
    Main()