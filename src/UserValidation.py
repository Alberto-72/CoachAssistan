# Here will validate all the parameters that indntify the user
import src.CommonFuntion as cf
import random

User_Data_Filename = "files/Data/UserData.csv"
User_Data_Fieldnames = ["UserName", "password", "rol", "key"]

class User:
    def __init__(self, username, password,rol):
        self.username = username # It cant be empty and may not be repited
        self.password = password # The pwd must have min 8 characters, 1 special character and 1 capital letter
        self.rol = rol # The user just would be Coach or player
    
    @property
    def username(self):
        return self._username
    @username.setter
    def username(self, username):
        if not username:
            raise ValueError("El nombre de usuario no puede estar vacío.")
        # Comprobar si existe ese nombre de ususario
        self._username = username
    
    def __str__(self):
        return f"Nombre de Usuario: {self.username}, Rol: {self.rol}"
    
def login():
    """Validate the user's login"""
    def TryPassword(username, pwd):
        alphabet = "áéíóúabcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ ,.;:!?'-_+()}{[]<=>|/\\~123456789" #Declaro un string con todos los caracteres del teclado
        dencripted = ""
        data = cf.ReadFile(User_Data_Filename)
        for row in data:
            if row["UserName"] == username: 
                pwd_encrypted = row["password"]
                key = int(row["key"])
                break
        else: raise ValueError("No se ha encontrado el nombre de usuario")
        for i in pwd_encrypted:
            pos = alphabet.find(i)
            if pos != -1:
                if pos-key < 0: #Como ahora estamos descifrando se resta a la posicion inicial la iteracion y si esta es menor que 0, nos va a dar erro
                    dencripted += alphabet[((pos-key)+len(alphabet))] #Ahora la letra que se va a guardar en descifrado sera la suma del numero negativo que da mas la longitud de la cadena
                else:
                    dencripted += alphabet[pos-key] #Si no es menor que 0, se suma a la cadena descifrada la letra del alfabeto en la posicion calculada
            else: dencripted += i #Si no es un caracter del alfabeto, se añade al mensaje descifrado como está
        if dencripted == pwd: return row["rol"]
        return None
    
    while True:
        cf.ClearScreen()
        print("--- LOGIN ---")
        username = input("Introduce tu nombre de usuario: ")
        password = input("Introduce tu contraseña: ")
        try:
            role = TryPassword(username, password)
            if role: 
                Current_User = User(username, password, role)
                return Current_User
            else: 
                raise ValueError("No se encuentra ningun usuario con dicha contraseña")
        except ValueError as e:
            print(e)
            op = input("Registrarse (S/N): ")
            if op.upper() == "S": register()
            else: continue

def register():
    def Encrypt(password):
        key = random.randint(0,100)
        alphabet = "áéíóúabcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ ,.;:!?'-_+()}{[]<=>|/\\~123456789" #Declaro un string con todos los caracteres del teclado
        encrypted = "" #Variable que va a almacenar el texto cifrado
        for i in password: #Recorro cada caracter del texto a cifrar
            pos = alphabet.find(i) #posicion inicial va a ser igual a la posición del caracter en el alfabeto
            if pos != -1:
                if pos+key > len(alphabet): #Si la posicion inicial mas la iteracion es mayor al tamaño del alfabeto, es decir si se va aimprimir erro debido a que no hay mas
                    encrypted += alphabet[(pos+key)%len(alphabet)] #Se calcula el resto de la division para que nos diga que posicion tiene que guardar, esta letra se la suma a las que haya en cifrado
                else:
                    encrypted += alphabet[pos+key] #En caso contrario, se suma a la cadena cifrada la letra del alfabeto en la posicion calculada
            else: encrypted += i #Si no es un caracter del alfabeto, se añade al mensaje cifrado como está
        return encrypted, key
    while True:
        try:
            cf.ClearScreen()
            print("--- REGISTRO ---")
            username = input("Introduce tu nombre de usuario: ")
            password = input("Introduce tu contraseña: ")
            password, key = Encrypt(password)
            rol = input("Introduce tu rol:\n1. Coach\n2. Player\nOpcion: ")
            if rol == "1": rol = "Coach"
            elif rol == "2": rol = "Player"
            else: raise ValueError("No has introducido un rol válido.")
            
            New_User = User(username, password, rol)
            break
        except ValueError as e:
            print(e)
    data = cf.ReadFile(User_Data_Filename)
    data.append({"UserName":New_User.username, "password":New_User.password, "rol":New_User.rol, "key":key})
    cf.WriteFile(User_Data_Filename, User_Data_Fieldnames ,data)
    