import tkinter as tk
root = tk.Tk()
root.geometry("400x50")

def setTextInput(text):
    textEntry.set(text)

textEntry = tk.StringVar()

textExample = tk.Entry(root,
                      textvariable = textEntry)
textExample.pack()

btnSet = tk.Button(root,
                   height=1,
                   width=10,
                   text="Set",
                   command=lambda:setTextInput("new content"))
btnSet.pack()

root.mainloop()