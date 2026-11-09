from tkinter import *
from tkinter import messagebox
import webbrowser
import os
import sys
from main import SupermarketApp
# background = "#1B3C53"
# framebg = "#234C6A"
# framefg = "#456882"
# fgvar= "#E3E3E3"
background = "#F4E7CD"
framebg = "#3A8376"
framefg = "#FFFFFF"
framebg2 = "#F4E7CD"
framefg2 = "#E59047"
bag = "#457157"

# Exit window
# def Exit():
#     window.destroy()

u1 = "https://www.facebook.com/profile.php?id=61581002406856"
u2 = "https://www.instagram.com/meriem.dv?igsh=MW1rbWwxbWZ3bTl4bw=="
u3 = "https://wa.me/212716359474"

def Open1():
    webbrowser.open_new(u1)

def Open2():
    webbrowser.open_new(u2)

def Open3():
    webbrowser.open_new(u3)

def about1():
    messagebox.showinfo("dévloppeur", "Meriem Elfilali")

def about2():
    messagebox.showinfo("projet", "Projet de Supermarché")

def log():
    user = En1.get()
    passw = En2.get()
    if user == "meriem" and passw == "2011":
        messagebox.showinfo("accueillir", "Bienvenue ! Les informations que vous avez saisies sont correctes.")
        # window.destroy()
        # root = Tk()
        # app = Super(root)
        # root.mainloop()
        # window.withdraw()
        # top = Toplevel()
        # SupermarketApp(top)
        window.destroy()   # نغلق نافذة login بالكامل

        root = Tk()        # ننشئ root جديد للتطبيق
        app = SupermarketApp(root)
        root.mainloop()

        
    elif not user or not passw:
        messagebox.showwarning("attention", "Vous devez saisir votre nom d'utilisateur et votre mot de passe.")
    else:
        messagebox.showerror("erreur", "Malheureusement, les données sont incorrectes.")
window =Tk()
window.geometry("1000x600+130+50")
window.config(bg=background)
window.resizable(False, False)
window.title("SuperMarché")
window.iconbitmap("images/shopping.ico")
Label(window, text="Super Marché System", width=10, height=2, bg= framebg, fg= framefg, font="tajawal 16 bold").pack(side=TOP, fill=X)
F1 = Frame(window, width=300, height=600, bg=bag)
F1.place(x=0, y=53)
Title1 = Label(F1, text="Projet de Supermarché", bg=bag, fg=framefg, font=("tajwal",12, "bold"))
Title1.place(x=42, y=50)
Title2 = Label(F1, text="Contactez-nous", bg=bag, fg=framefg, font=("tajwal",12, "bold"))
Title2.place(x=42, y=100)

B1 = Button(F1, text="Notre Compte Facabook", width=26, fg=framebg2, bg=bag, font="tajwal 11 bold", bd=0, activebackground=framefg2, activeforeground="black", command=Open1)
B1.place(x=10, y=160)
B2 = Button(F1, text="Notre Compte Instagram", width=26, fg=framebg2, bg=bag, font="tajwal 11 bold", bd=0, activebackground=framefg2, activeforeground="black", command=Open2)
B2.place(x=10, y=220)
B3 = Button(F1, text="Notre Compte WhatsApp", width=26, fg=framebg2, bg=bag, font="tajwal 11 bold", bd=0, activebackground=framefg2, activeforeground="black", command=Open3)
B3.place(x=10, y=280)
B4 = Button(F1, text="A propos du dévloppeur", width=26, fg=framebg2, bg=bag, font="tajwal 11 bold", bd=0, activebackground=framefg2, activeforeground="black", command=about1)
B4.place(x=10, y=340)
B5 = Button(F1, text="Aperçu du programme", width=26, fg=framebg2, bg=bag, font="tajwal 11 bold", bd=0, activebackground=framefg2, activeforeground="black", command=about2)
B5.place(x=6, y=400)
B6 = Button(F1, text="Fermer le Programme", width=26, fg=framebg2, bg=bag, font="tajwal 11 bold", bd=0, command=quit, activebackground=framefg2, activeforeground="black")
B6.place(x=6, y=460)

photo = PhotoImage(file="images/supermarket.png")
img=Label(window, image=photo, bg=background)
img.place(x=500, y=55, width=308, height=272)

F2 = Frame(window, width=650, height=200, bg=bag)
F2.place(x=325, y=350)
photo1 = PhotoImage(file="images/key-person (2).png")
img1 = Label(window, image=photo1, bg=bag)
img1.place(x=350, y=370, width=120, height=150)
L1 = Label(F2, text="Nom D'utilisateur ", fg=framebg2, bg=bag, font="tajawal 12")
L1.place(x=150, y=50)
L2 = Label(F2, text="Mot de passe ", fg=framebg2, bg=bag, font="tajawal 12")
L2.place(x=150, y=100)
En1 = Entry(F2, font="tajawal 12", justify="center", highlightthickness=2, highlightbackground=framebg, highlightcolor=framefg2)
En1.place(x=300, y=50)
En2 = Entry(F2, font="tajawal 12", justify="center", highlightthickness=2, highlightbackground=framebg, highlightcolor=framefg2, show="*")
En2.place(x=300, y=100)
B = Button(F2, text="Se Connecter", fg=framebg, bg=framebg2, font="tajawal 10", width=22, height=1, activebackground=framefg2, activeforeground="black", bd=0, command=log)
B.place(x=303, y=140)



window.mainloop()
