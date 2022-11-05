import tkinter as tk

def dowhy_checkbox_values():
    value = []
    text=[]
    for cb, var in zip(checkbuttons, vars):
        if var.get() == 1:
            text.append(cb.cget("text"))
        #value.append(var.get())
        #print("%s: %d" % (text, value))
    #print(value)
    print(text)
root = tk.Tk()
text = tk.Text(root, cursor="arrow")
vsb = tk.Scrollbar(root, command=text.yview)
button = tk.Button(root, text="Get Values", command= lambda: dowhy_checkbox_values())
text.configure(yscrollcommand=vsb.set)

button.pack(side="top")
vsb.pack(side="right", fill="y")
text.pack(side="left", fill="both", expand=True)

checkbuttons = []
vars = []
for i in range(20):
    var = tk.IntVar(value=0)
    cb = tk.Checkbutton(text, text="checkbutton #%s" % i,
                        variable=var, onvalue=1, offvalue=0)
    text.window_create("end", window=cb)
    text.insert("end", "\n")
    checkbuttons.append(cb)
    vars.append(var)
text.configure(state="disabled")

root.mainloop()


