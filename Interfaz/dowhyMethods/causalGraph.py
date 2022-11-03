def generateCausalGraph(model):
    img_path = "./Interfaz/img/causal_graph"
    model.view_model(file_name = img_path)

    return img_path + ".png"
    