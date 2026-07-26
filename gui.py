import tkinter as tk
from tkinter import messagebox
import main
import string
import secrets


# ---------- Theme ----------

BG_COLOR = "#101820"
FG_COLOR = "#00FF99"
BUTTON_COLOR = "#1F4E79"
TEXT_COLOR = "white"


# ---------- Login ----------

def login():

    password = password_entry.get()

    try:
        with open("master.hash", "r") as file:
            stored_hash = file.read()

    except FileNotFoundError:

        messagebox.showerror(
            "Error",
            "Master password not created"
        )
        return


    if main.verify_password(password, stored_hash):

        messagebox.showinfo(
            "Success",
            "Login Successful"
        )

        open_vault()

    else:

        messagebox.showerror(
            "Error",
            "Incorrect Password"
        )



# ---------- Generate Password ----------

def generate_password():

    chars = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = ""

    for i in range(16):
        password += secrets.choice(chars)


    messagebox.showinfo(
        "Generated Password",
        password
    )



# ---------- Add Password ----------

def add_password_gui():

    add_window = tk.Toplevel(window)

    add_window.title(
        "Add Password"
    )

    add_window.geometry(
        "400x400"
    )

    add_window.configure(
        bg=BG_COLOR
    )


    tk.Label(
        add_window,
        text="Website",
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)


    website_entry = tk.Entry(
        add_window
    )

    website_entry.pack()



    tk.Label(
        add_window,
        text="Username",
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)


    username_entry = tk.Entry(
        add_window
    )

    username_entry.pack()



    tk.Label(
        add_window,
        text="Password",
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=5)


    password_entry = tk.Entry(
        add_window,
        show="*"
    )

    password_entry.pack()



    def save():

        website = website_entry.get()
        username = username_entry.get()
        password = password_entry.get()


        if website == "" or username == "" or password == "":

            messagebox.showerror(
                "Error",
                "Fill all fields"
            )

            return


        encrypted = main.cipher.encrypt(
            password.encode()
        ).decode()


        main.passwords[website] = {

            "username": username,
            "password": encrypted

        }


        main.save_passwords(
            main.passwords
        )


        messagebox.showinfo(
            "Success",
            "Password Saved"
        )


        add_window.destroy()



    tk.Button(
        add_window,
        text="SAVE PASSWORD",
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        width=20,
        command=save
    ).pack(pady=20)




# ---------- View Password ----------

def view_passwords():

    data = ""


    for website, details in main.passwords.items():

        password = main.cipher.decrypt(
            details["password"].encode()
        ).decode()


        data += (
            f"Website : {website}\n"
            f"Username: {details['username']}\n"
            f"Password: {password}\n\n"
        )


    if data == "":
        data = "No passwords saved"


    messagebox.showinfo(
        "Password Vault",
        data
    )




# ---------- Delete Password ----------

def delete_password_gui():

    website = delete_entry.get()


    if website in main.passwords:

        del main.passwords[website]


        main.save_passwords(
            main.passwords
        )


        messagebox.showinfo(
            "Success",
            "Password Deleted"
        )


    else:

        messagebox.showerror(
            "Error",
            "Website not found"
        )




# ---------- Vault ----------

def open_vault():

    login_frame.destroy()


    vault = tk.Frame(
        window,
        bg=BG_COLOR
    )

    vault.pack(
        pady=30
    )


    tk.Label(
        vault,
        text="🔐 SECURE PASSWORD VAULT",
        font=("Arial",20,"bold"),
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=20)



    buttons = [

        ("Add Password", add_password_gui),

        ("View Passwords", view_passwords),

        ("Generate Password", generate_password),

    ]


    for text, command in buttons:

        tk.Button(
            vault,
            text=text,
            width=25,
            height=2,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            font=("Arial",11,"bold"),
            command=command
        ).pack(pady=5)



    tk.Label(
        vault,
        text="Delete Website",
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=10)



    global delete_entry


    delete_entry = tk.Entry(
        vault
    )

    delete_entry.pack()



    tk.Button(
        vault,
        text="DELETE PASSWORD",
        width=25,
        height=2,
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        command=delete_password_gui
    ).pack(pady=10)



    tk.Button(
        vault,
        text="EXIT",
        width=25,
        height=2,
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        command=window.destroy
    ).pack(pady=10)




# ---------- Main Window ----------

window = tk.Tk()

window.title(
    "🔐 Cyber Secure Password Manager"
)


window.geometry(
    "550x600"
)


window.configure(
    bg=BG_COLOR
)



login_frame = tk.Frame(
    window,
    bg=BG_COLOR
)

login_frame.pack(
    pady=150
)



tk.Label(
    login_frame,
    text="🔐 MASTER PASSWORD",
    font=("Arial",16,"bold"),
    bg=BG_COLOR,
    fg=FG_COLOR
).pack(pady=10)



password_entry = tk.Entry(
    login_frame,
    show="*",
    font=("Arial",14),
    bg="black",
    fg="white"
)

password_entry.pack()



tk.Button(
    login_frame,
    text="LOGIN",
    width=20,
    height=2,
    bg=BUTTON_COLOR,
    fg=TEXT_COLOR,
    font=("Arial",12,"bold"),
    command=login
).pack(pady=20)



window.mainloop()