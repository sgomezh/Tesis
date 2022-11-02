def generateCausalGraph(model):
    model.view_model()
    from IPython.display import Image, display
    display(Image(filename="causal_model.png"))
    showCausalGraph()

def showCausalGraph():
    from PIL import Image, ImageTk
    from tkinter import Canvas
    from tkinter import NW

    img = Image.open("causal_model.png")
    causal_graph_canvas = Canvas(width= 550, height= 440)
    causal_graph_canvas.place(x=300, y=100)
    img = Image.open("causal_model.png")
    resize_img = img.resize((500, 400), Image.ANTIALIAS)
    causal_graph = ImageTk.PhotoImage(resize_img)
    causal_graph_canvas.create_image(0, 0, anchor='nw', image=causal_graph)
    causal_graph_canvas.image = causal_graph