# COACH ASSISTANT

import src.CommonFuntion as cf
import src.UserValidation as uv
import src.Team as T
from src.Practices import PracticesMenu
from src.Player import PlayerMenu
from src.Games import GamesMenu

def Main():
    """Main menu of the application"""
    while True:
        cf.ClearScreen()
        print("--- COACH ASSISTANT ---")
        print("1. Iniciar sesión")
        print("2. Registrar")
        print("3. Salir")

        option = input("Elija una opción: ")

        match option:
            case "1":
                user = uv.login()
                if user:  # Si el login es exitoso
                    MainMenu(user)
            case "2":
                uv.register()
            case "3":
                print("¡Adiós!")
                break
            case _:
                print("Opción inválida. Intente de nuevo.")
                input("Presione Enter para continuar...")  # Para evitar que el mensaje desaparezca inmediatamente

def MainMenu(user):
    """Main menu for logged-in users"""
    while True:
        cf.ClearScreen()
        print(f"Bienvenido {user.username} como {user.rol}!")

        # Selección de equipo
        Team = None
        while not Team:
            Team = T.SelectTeam(user)
            if not Team:
                print("No seleccionaste un equipo válido.")
                retry = input("¿Intentar de nuevo? (S/N): ").strip().upper()
                if retry != "S":
                    return

        print("\n--- MENÚ PRINCIPAL ---")
        print("1. MENU ENTRENOS")
        print("2. MENU JUGADORES")
        print("3. MENU PARTIDOS")
        print("4. SALIR")

        op = input("Opción: ")

        match op:
            case "1": PracticesMenu()
            case "2": PlayerMenu(Team)
            case "3": GamesMenu(Team)
            case "4":
                print("Saliendo...")
                break
            case _:
                print("Opción inválida. Intente de nuevo.")
                input("Presione Enter para continuar...")  # Pausa antes de refrescar pantalla

if __name__ == '__main__':
    Main()