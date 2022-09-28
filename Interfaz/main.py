
#import statement
from ast import main
import tkinter as tk
from tkinter.font import Font
from PIL import Image, ImageTk

# ----------------------- SETTINGS ----------------------

#create GUI Tk() variable
main_page = tk.Tk()
#set title
main_page.title("Causal Tool")
#set icon
icon = Image.open('Interfaz/icon.png')
photo = ImageTk.PhotoImage(icon)
main_page.wm_iconphoto(False, photo)
#set window size
main_page.state('zoomed')
#set window background color
main_page.configure(background='#08013D')
#obtain screen width and height
'''altura = main_page.winfo_reqheight()
anchura = main_page.winfo_reqwidth()'''
#obtain screen resolution
anchura = main_page.winfo_screenwidth()
altura  = main_page.winfo_screenheight()
#set fonts
label_font = Font(family="Arabic Transparent", size=25, weight="bold")
button_font = Font(family="Arabic Transparent", size=12, weight="bold")

# ---------------------- INTERFACE ----------------------
#image
image = Image.open('Interfaz/causal_tool.png')
logo = ImageTk.PhotoImage(image)
label = tk.Label(main_page, image=logo)
label.image = logo
label.place(x=anchura-1200, y=10)
#label BART
bart_label = tk.Label(main_page, text="BART", font=label_font, bg='#08013D', fg='#FFFFFF')
bart_label.place(x=50, y=50)
#label DoWhy
dowhy_label = tk.Label(main_page, text="DoWhy", font=label_font, bg='#08013D', fg='#FFFFFF')
dowhy_label.place(x=anchura-180, y=50)
#buttons BART
button2 = tk.Button(main_page, text="Predict", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button2.place(x=10, y=130)

button3 = tk.Button(main_page, text="RMSE", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button3.place(x=10, y=210)

button4 = tk.Button(main_page, text="Variable \nImportance", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button4.place(x=10, y=290)
'''
button5 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button5.place(x=10, y=370)

button6 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button6.place(x=10, y=450)

button7 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button7.place(x=10, y=530)

button8 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button8.place(x=10, y=610)'''

#buttons DoWhy
button2 = tk.Button(main_page, text="Get ATE", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button2.place(x=anchura-225, y=130)

button3 = tk.Button(main_page, text="GML Graph", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button3.place(x=anchura-225, y=210)

button4 = tk.Button(main_page, text="Estimate effect", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button4.place(x=anchura-225, y=290)

button5 = tk.Button(main_page, text="Refute result", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button5.place(x=anchura-225, y=370)
'''
button6 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button6.place(x=1150, y=450)

button7 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button7.place(x=1150, y=530)

button8 = tk.Button(main_page, text="Click Me!", bg="#B7B5C8", fg="black", font=button_font, width=20, height=3)
button8.place(x=1150, y=610)'''

#show window
main_page.mainloop() 