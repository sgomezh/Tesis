

def generateCausalGraph(model):
    model.view_model()
    from IPython.display import Image, display
    display(Image(filename="causal_model.png"))

