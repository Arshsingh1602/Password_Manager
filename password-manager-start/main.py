from tkinter import *
import os
import random
import pyperclip
import json

BG_COLOUR = "#C5EBAA"
ADD_BUTTON_COLOR = "#AAC8A7"
email_data = ""
default_email = ""
password_save = ""
website_save= ""
email_save = ""
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():

    password_entry.delete(0,'end')

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for char in range(nr_letters)]
    password_symbols = [random.choice(symbols) for char in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for char in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = ""
    for char in password_list:
      password += char

    password_entry.insert(0,password)

    pyperclip.copy(password)
    pyperclip.paste()


# ---------------------------- SAVE PASSWORD ------------------------------- #

def clear():
    website_entry.delete(0,"end")
    password_entry.delete(0, "end")
    website_entry.focus()

def succesful():
    popup_1 = Toplevel(window,bg=BG_COLOUR)
    popup_1.title("Success")
    success_label = Label(popup_1,text="Password Successfully Saved",font=(20),pady=10,padx=10, bg=BG_COLOUR)
    success_label.pack()
    popup_1.after(1000,lambda:popup_1.destroy())

def save():
    website_save = website_entry.get()
    email_save = email_entry.get()
    password_save = password_entry.get()
    new_data = {
        website_save:{
            "email": email_save,
            "password": password_save,
        }
    }
    if website_save == "" or email_save == "" or password_save == "" :
        popup_2 = Toplevel(window, bg=BG_COLOUR)
        popup_2.title("Error")
        success_label = Label(popup_2,text="Required fields cannot be empty", font=(20), pady=10, padx=10, bg=BG_COLOUR)
        success_label.pack()
        popup_2.after(1500, lambda: popup_2.destroy())
    else:
        try:
            with open("data.json","r") as saved:
                d = json.load(saved)
        except FileNotFoundError:
            with open(data.json,"w") as saved:
                json.dump(new_data,saved,indent=4)

        else:
            d.update(new_data)
            with open(data.json,"w") as saved:
                json.dump(d,saved,indent=4)
        finally:
            succesful()
            clear()
# ---------------------------FIND PASSWORD----------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except:
        messagebox.showinfo(title="Error",message="File not found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password}")
        else:
            messagebox.showinfo(title="Error",message=f"No info about the {website}")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20,pady=20,bg=BG_COLOUR)

if os.path.getsize("email.txt") == 0:

    global popup
    popup = Toplevel(window,bg=BG_COLOUR,padx=7,pady=5)
    popup.title("Record Email")


    def write_email():
        global email_data
        with open("email.txt", "w") as w:
            w.write(f"{email_data}")

    def close_toplevel():
        if popup:
            popup.destroy()
            window.attributes('-topmost', 1)

    def get_data():
        global email_data
        email_data = regular_email_entry.get()
        close_toplevel()
        write_email()

    regular_email = Label(popup, text="Enter your regular email: ",bg=BG_COLOUR,pady=10)
    regular_email.grid(row=0,column=0)

    regular_email_entry = Entry(popup)
    regular_email_entry.grid(row=0,column=1)
    regular_email_entry.focus()

    submit_button = Button(popup,text="Submit",bg=ADD_BUTTON_COLOR,command=get_data)
    submit_button.grid(row=1,column=0,columnspan=2)

    popup.after(100,popup.lift)

with open("email.txt","r") as r:
    default_email = r.readline()

canvas = Canvas(width=200, height=200, bg=BG_COLOUR, highlightthickness=0)
image = PhotoImage(file="logo.png")
canvas.create_image(115, 100, image=image)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:", bg=BG_COLOUR, pady=2)
website_label.grid(row=1, column=0)

website_entry = Entry(width=51)
website_entry.grid(row=1, column=1, sticky=W)
if os.path.getsize("email.txt") != 0:
    website_entry.focus()

email_label = Label(text="Email/Username:", bg=BG_COLOUR, pady=4)
email_label.grid(row=2, column=0)

email_entry = Entry(width=51)
email_entry.grid(row=2, column=1, columnspan=2, sticky=W)
email_entry.insert(0, default_email)


password_label = Label(text="Password:", bg=BG_COLOUR)
password_label.grid(row=3, column=0)

password_entry = Entry(width=32)
password_entry.grid(row=3, column=1, sticky=W)


password_button = Button(text="Generate Password", width=14, bg=ADD_BUTTON_COLOR,command=generate_password)
password_button.grid(row=3, column=2, sticky=W)

add_button = Button(text="Add", width=43, bg=ADD_BUTTON_COLOR,command=save)
add_button.grid(row=4, column=1, columnspan=2, pady=4)

search_button = Button(text="Search",width=14, bg=ADD_BUTTON_COLOR)
search_button.grid(row=2,column=2,columnspan=2,pady=4)

window.mainloop()
