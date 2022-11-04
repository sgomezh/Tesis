def generateCausalGraph(model):
    print(model.view_model.__code__.co_varnames)
    img_path = "./Interfaz/img/causal_graph"
    model.view_model(file_name = img_path)
    return img_path + ".png"
    