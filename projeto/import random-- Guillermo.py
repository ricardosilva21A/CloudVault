import hashlib

def hash_password(password):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode("utf-8"))
    return sha256_hash.hexdigest()

def store_password(username, site, password):
    hashed_password = hash_password(password)
    f=open("passwords.txt", "a")
    if (f==IOError):
        print("Aperture error")
    else:            
        f.write(f"{username}:{site}:{hashed_password}\n")
        print("Password stored correctly")

def verify_usr(username, site):
    f=open("passwords.txt", "r")
    if (f==IOError):
        print("Aperture error")
    else:         
        ctrl=0
        for line in f.readlines():
            stored_username, stored_site, _ = line.strip().split(":")
            if username == stored_username and site == stored_site:
                ctrl=1
    return ctrl

# Example usage:
def new_user():
    username = input("Enter a username: ")
    site = input("Enter a site: ")
    if verify_usr(username, site):
        print("\nUser already registred")
    else :  
        password = input("Enter a password: ")
        store_password(username, site, password)
        print("User successfully created")
             
def change_pass():
    username = input("Enter a username: ")
    site = input("Enter a site: ")
    if verify_usr(username, site):      
        with open("passwords.txt", "r") as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            stored_username, stored_site, _ = line.strip().split(":")
            if username!= stored_username or site!= stored_site:
                new_lines.append(line)
        
        password = input("Enter the new password: ")
        
        with open("passwords.txt", "w") as f:
            f.writelines(new_lines)    
        store_password(username, site, password)       
    else:
        print("User not found")

def menu():
    ans=0
    f=open("passwords.txt", "a")
    if (f==IOError):
        print("Aperture error")
    else:
        while (ans!="6"):
            print("\n1.Add a password")
            print("2.Change a Student")
            print("3.Look Up Student Record")
            print("4.")
            print("5.")
            print("6.Exit program")
            ans=input("\nWhat would you like to do?\n")
            if ans=="1": 
                new_user()
            elif ans=="2":
                change_pass()
            elif ans=="3":
                print("\n Student Record Found") 
            elif ans=="6":
                print("\n Goodbye")

menu()