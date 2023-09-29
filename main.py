from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import sqlite3


def create_table():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS passwords (website TEXT, email TEXT, password TEXT)')
    conn.commit()
    conn.close()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('SELECT * FROM passwords WHERE website=:website AND email=:email',
                  {'website': website, 'email': email})
        existing_entry = c.fetchone()
        if existing_entry is None:
            c.execute('INSERT INTO passwords VALUES (:website, :email, :password)', {
                      'website': website, 'email': email, 'password': password})
            conn.commit()
            website_entry.delete(0, END)
            password_entry.delete(0, END)
        else:
            messagebox.showinfo(
                title="Oops", message="An entry for this website and email already exists.")
        conn.close()

# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website = website_entry.get()
    email = email_entry.get()
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM passwords WHERE website=:website AND email=:email',
              {'website': website, 'email': email})
    result = c.fetchone()
    conn.close()

    if result:
        password = result[2]
        messagebox.showinfo(
            title=website, message=f"Email: {email}\nPassword: {password}")
    else:
        messagebox.showinfo(
            title="Error", message=f"No details for {website} with the email {email} exists.")


# ---------------------------- DELETE PASSWORD ------------------------------- #
def delete_password():
    website = website_entry.get()
    email = email_entry.get()  # get email as well

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Check if the record exists
    c.execute('SELECT * FROM passwords WHERE website=:website AND email=:email',
              {'website': website, 'email': email})
    result = c.fetchone()

    if result is None:
        messagebox.showinfo(
            title="Error", message=f"No details for {website} associated with {email} exists.")
    else:
        # Delete by website and email
        c.execute('DELETE FROM passwords WHERE website=:website AND email=:email',
                  {'website': website, 'email': email})

        conn.commit()
        messagebox.showinfo(
            title="Success", message=f"Deleted details for {website} associated with {email}")
    conn.close()


# ---------------------------- LIST WEBSITES ------------------------------- #
def list_websites():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM passwords')
    data = c.fetchall()
    conn.close()

    if data:
        websites_and_emails = "\n".join(
            [f"Website: {row[0]}\nEmail: {row[1]}\n---" for row in data])
        messagebox.showinfo(title="Websites and Emails",
                            message=f"Websites and Emails:\n\n{websites_and_emails}")
    else:
        messagebox.showinfo(title="Error", message="No data found.")


# ---------------------------- CLEAR ALL FIELDS ------------------------------- #
def clear_all():
    website_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "rahul@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=2)
generate_password_button = Button(
text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)
delete_button = Button(text="Delete", width=36, command=delete_password)
delete_button.grid(row=5, column=1, columnspan=2)
list_button = Button(text="List Websites", width=36, command=list_websites)
list_button.grid(row=6, column=1, columnspan=2)
clear_button = Button(text="Clear All", width=36, command=clear_all)
clear_button.grid(row=7, column=1, columnspan=2)

create_table()

window.mainloop()
