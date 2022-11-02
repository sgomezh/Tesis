def generateCausalGraph(model):
    model.view_model()
    from IPython.display import Image, display
    img_path = "causal_model.png"
    display(Image(filename=img_path))
    #showCausalGraph()
    return img_path
    