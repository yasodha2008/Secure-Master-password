import requests
import base64
import hashlib
import os
import time
import json
import string
import secrets
from cryptography.fernet import Fernet


# ---------- Password Strength Checker ----------

def check_password_strength(password):

    score = 0

    if len(password) >= 8:
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(char in string.punctuation for char in password):
        score += 1


    if score == 5:
        return "Strong Password"

    elif score >= 3:
        return "Medium Password"

    else:
        return "Weak Password"



# ---------- Master Password Hashing ----------

def hash_password(password):

    salt = os.urandom(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )

    return (
        base64.b64encode(salt).decode()
        + ":"
        + base64.b64encode(hashed).decode()
    )


def verify_password(password, stored):

    salt, old_hash = stored.split(":")

    salt = base64.b64decode(salt)
    old_hash = base64.b64decode(old_hash)


    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        100000
    )


    return new_hash == old_hash



def create_master_password():

    if not os.path.exists("master.hash"):

        print("First time setup")

        password = input("Create Master Password: ")

        hashed = hash_password(password)

        with open("master.hash", "w") as file:
            file.write(hashed)

        print("Master Password Created Successfully!\n")



def master_login():

    with open("master.hash","r") as file:
        stored_hash = file.read()


    password = input("Enter Master Password: ")


    if verify_password(password, stored_hash):

        print("Login Successful!\n")

    else:

        print("Incorrect Password!")
        exit()



# ---------- Encryption ----------

def load_key():

    if os.path.exists("secret.key"):

        with open("secret.key","rb") as file:
            return file.read()

    else:

        key = Fernet.generate_key()

        with open("secret.key","wb") as file:
            file.write(key)

        return key



key = load_key()

cipher = Fernet(key)



# ---------- Database ----------

def load_passwords():

    if os.path.exists("passwords.json"):

        try:

            with open("passwords.json","r") as file:
                return json.load(file)

        except:

            return {}

    return {}



def save_passwords(passwords):

    with open("passwords.json","w") as file:
        json.dump(passwords,file,indent=4)


passwords = load_passwords()
last_activity = time.time()



# ---------- Password Generator ----------

def generate_password(length=16):

    chars = string.ascii_letters + string.digits + string.punctuation

    return ''.join(secrets.choice(chars) for _ in range(length))


def check_breach(password):

    sha1_password = hashlib.sha1(
        password.encode()
    ).hexdigest().upper()


    prefix = sha1_password[:5]
    suffix = sha1_password[5:]


    url = f"https://api.pwnedpasswords.com/range/{prefix}"


    response = requests.get(url)


    if response.status_code != 200:
        print("Could not check breach database")
        return False


    hashes = response.text.splitlines()


    for line in hashes:

        hash_suffix, count = line.split(":")

        if hash_suffix == suffix:

            print(
                f"⚠️ Password found in {count} breaches!"
            )

            return True


    print("✅ Password not found in breaches")

    return False
# ---------- Add Password ----------

def add_password():

    website = input("Website: ")

    username = input("Username: ")


    print("\n1. Enter your own password")
    print("2. Generate password")


    choice = input("Choose: ")


    if choice == "1":

        password = input("Password: ")

        check_breach(password)

        print("Password Strength:",
              check_password_strength(password))


    else:

        password = generate_password()

        print("Generated Password:",password)

        print("Password Strength:",
              check_password_strength(password))



    encrypted = cipher.encrypt(password.encode()).decode()


    passwords[website] = {

        "username":username,
        "password":encrypted

    }


    save_passwords(passwords)

    print("Password saved successfully!")



# ---------- View Password ----------

def view_passwords():

    if not passwords:

        print("No passwords saved.")
        return


    for website,details in passwords.items():

        password = cipher.decrypt(
            details["password"].encode()
        ).decode()


        print("\n--------------------")
        print("Website :",website)
        print("Username:",details["username"])
        print("Password:",password)




# ---------- Search ----------

def search_password():

    website = input("Enter website: ")


    if website in passwords:

        password = cipher.decrypt(
            passwords[website]["password"].encode()
        ).decode()


        print("\nWebsite :",website)
        print("Username:",passwords[website]["username"])
        print("Password:",password)


    else:

        print("Website not found!")




# ---------- Update ----------

def update_password():

    website=input("Enter website to update: ")


    if website in passwords:

        username=input("New Username: ")

        password=input("New Password: ")


        print("Password Strength:",
              check_password_strength(password))


        encrypted=cipher.encrypt(
            password.encode()
        ).decode()


        passwords[website]={

            "username":username,
            "password":encrypted

        }


        save_passwords(passwords)

        print("Updated Successfully!")


    else:

        print("Website not found!")




# ---------- Delete ----------

def delete_password():

    website=input("Enter website to delete: ")


    if website in passwords:

        del passwords[website]

        save_passwords(passwords)

        print("Deleted Successfully!")

    else:

        print("Website not found!")




# ---------- Main ----------

def check_auto_lock():

    global last_activity

    current_time = time.time()

    if current_time - last_activity > 120:

        print("\nVault locked due to inactivity!")

        master_login()

    last_activity = current_time



if __name__ == "__main__":

    create_master_password()

    master_login()


    while True:

        check_auto_lock()

        print("\n====== PASSWORD MANAGER ======")

        print("1. Add Password")
        print("2. View Passwords")
        print("3. Generate Password")
        print("4. Search Password")
        print("5. Update Password")
        print("6. Delete Password")
        print("7. Exit")


        choice = input("Enter your choice: ")


        if choice == "1":
            add_password()

        elif choice == "2":
            view_passwords()

        elif choice == "3":
            print("Generated Password:",
                  generate_password())

        elif choice == "4":
            search_password()

        elif choice == "5":
            update_password()

        elif choice == "6":
            delete_password()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid Choice!")