from re import search
from tkinter import *
from tkinter import messagebox
from secrets import randbelow,choice
import pyperclip
import json
#-------------------------PASSWORD GENERATOR----------------------#
def password_generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_password = [choice(letters) for _ in range(8 + randbelow(3))] #Password has minimum of eight letters
    symbols_password =  [choice(numbers) for _ in range(2 + randbelow(3))]
    numbers_password =  [choice(symbols) for _ in range(2 + randbelow(3))]
    password_list = letters_password + symbols_password + numbers_password
    #Shuffling the password
    for i in range(len(password_list) - 1, 0, -1):
            j = randbelow(i + 1)  # 0 ≤ j ≤ i
            password_list[i], password_list[j] = password_list[j], password_list[i]

    password = "".join(password_list)
    password_entry.insert(0,password)
    pyperclip.copy(password)#Copies password to clipboard

#---------------------------SAVE PASSWORD-------------------------#
def save_data_to_file():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website:{
        "email":email,
        "password":password
    }
    }

    if len(website) ==0 or len(password) == 0:
        messagebox.showerror(title = "Fields left empty", message="Please ensure that no field is empty")
    # else:
    #     is_ok = messagebox.askokcancel(title = website_entry.get(),message = f"These are the details you entered : \n\nEmail : {email}\nPassword : {password}\n\nIs it okay to save?")
    #     if is_ok:
    #         with open("data.txt","a") as file:
    #             data_line = f"{website} | {email} | {password}"
    #             file.write(data_line+"\n")
    #             website_entry.delete(0,END)
    #             password_entry.delete(0,END)
    #             website_entry.focus()

    #USING JSON

    else:
        try:
            with open("data.json","r") as file:
                data = json.load(file)#reading old data
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data,file,indent = 2)
        else:
            data.update(new_data)#adding new data
            with open("data.json", "w") as file:
                json.dump(data, file, indent=2)
        finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                website_entry.focus()

def search_file():
    try:
        with open("data.json","r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error",message = "File doesn't have any existing data" )
    else:
        website = website_entry.get()
        if website in data:
            messagebox.showinfo(title = "Info", message=f"Website : {website}\nEmail : {data[website]["email"]}\nPassword : {data[website]["password"]}")
        else:
            messagebox.showerror(title="Invalid Website", message="File doesn't have data pertaining to this website")



# ----------------------------UI SETUP----------------------------#
window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)

canvas = Canvas(width = 300, height = 300)
padlock = PhotoImage(file = "padlock.png")
canvas.create_image(110,150,image = padlock)
canvas.grid(column = 1, row = 0)

website_label = Label(text = "Website : ", font=("Courier", 11))
website_label.grid(column = 0, row = 1)
website_entry = Entry(width = 48)
website_entry.focus()
website_entry.grid(column = 1, row = 1)

email_label = Label(text = "Email/Username : ",font=("Courier", 11))
email_label.grid(column = 0, row = 2)
email_entry = Entry(width = 70)
email_entry.insert(0, "abc@gmail.com")
email_entry.grid(column = 1, row = 2, columnspan=2)

password_label = Label(text = "Password : ", font = ("Courier", 11))
password_label.grid(column = 0, row = 3)
password_entry = Entry(width = 48)
password_entry.grid(column = 1, row = 3)

gen_password_button = Button(text = "Generate Password", font = ("Courier", 9), command=password_generate)
gen_password_button.grid(column = 2, row = 3)

add_button = Button(width = 61, text = "Add",font = ("Courier", 9), command = save_data_to_file)
add_button.grid(column = 1, row = 4, columnspan=2)

search_button = Button(text = "Search",font = ("Courier", 9),width = 15, command = search_file)
search_button.grid(column = 2, row = 1)

window.mainloop()

