from typing import List

import pygame
import node as n
import random
import math
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from camera import Camera


# Necesita graphviz pero de C y pygraphviz de python. usar:
# pip3 install --install-option="--include-path=/usr/local/include/"
# --install-option="--library-path=/usr/local/lib/" pygraphviz

class NodeManipulator:
    # Lista de nodos
    nodes: List[n.Node]  # Nodos ordenados
    nodes_bd: List[List[n.Node]]  # Nodos ordenados por la profundidad

    # Nodo seleccionado (Debajo del puntero)
    node_selected: [n.Node]

    # Fuente y texto de informacion del nodo seleccionado
    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
    text: pygame.font.Font

    # Camara
    camera: Camera

    def __init__(self, root_node: n.Node):
        self.nodes = [root_node]
        self.nodes_bd = [[root_node]]
        self.camera = Camera()
        self.node_selected = None
        pass

    def update(self) -> None:
        """
        Actualiza los nodos almacenados
        """
        for node in self.nodes:
            node.update()

        self.camera.update()

        # Nodo en la posicion del mouse
        m_pos = pygame.mouse.get_pos()
        pre_node_selected = self.node_selected
        self.node_selected = self.in_node(m_pos[0], m_pos[1])

        # Deseleccionando nodo que estaba seleccionado
        if pre_node_selected is not self.node_selected and pre_node_selected:
            pre_node_selected.selected = False

        # Actualizando informacion del nodo seleccionado
        if self.node_selected is not None:
            self.node_selected.selected = True
            self.text = self.font.render("Nodo: " + str(self.node_selected.id),
                                         True, (255, 200, 200),
                                         (40, 40, 40))
        else:
            self.text = self.font.render("", True, (255, 200, 200), )

    def draw(self, surface: pygame.Surface) -> None:
        """
        Dibuja los nodos almacenados
        :param surface: Superficie donde se van a dibujar los nodos
        """
        for node in self.nodes:
            node.draw(surface, self.camera)

        m_pos = pygame.mouse.get_pos()
        surface.blit(self.text, (m_pos[0] + 10, m_pos[1]))

    def generate_son(self, clic_x: int, clic_y: int) -> None:
        """
        Genera un nodo hijo conectado con el nodo al que se hace clic
        :param clic_x:  Posicion del clic en el eje X
        :param clic_y:  Posicion del clic en el eje Y
        """
        for node in self.nodes:
            if node.in_body(clic_x, clic_y, self.camera):
                # Generando nuevo nodo
                color = [200, 200, 200]
                angle_objetive = random.random() * 2 * math.pi

                pos_objetive = (math.sin(angle_objetive) * node.radius * 5 +
                                node.pos[0], math.cos(angle_objetive) *
                                node.radius * 5 + node.pos[1])
                id_nodo = len(self.nodes)
                new_node = node.generate_son([node.pos[0], node.pos[1]], color,
                                             pos_objetive, id_nodo)

                # Agregando el nuevo nodo a la lista de nodos ordenado por
                # profundidad
                if len(self.nodes_bd) < new_node.depth:
                    # Agrandando lista de litas de nodos (profundidad)
                    self.nodes_bd.append([])
                i_father = self.nodes_bd[node.depth - 1].index(node)

                encontrado = False
                for n in self.nodes_bd[new_node.depth - 1]:
                    i_nfather = self.nodes_bd[n.father.depth - 1].index(
                        n.father)
                    if i_nfather > i_father:
                        index_n = self.nodes_bd[n.depth - 1].index(n)
                        self.nodes_bd[new_node.depth - 1].insert(index_n,
                                                                 new_node)
                        encontrado = True
                        break
                if not encontrado:
                    self.nodes_bd[new_node.depth - 1].append(new_node)

                # Agregando el nuevo nodo a la lista de nodos
                self.nodes.append(new_node)
                break
        self.update_position()

    def update_position(self) -> None:
        """
        Actualiza la posicion de todos los nodos, generando una estructura de
        arbol con estos.
        """
        SIZE = self.camera.anchura
        SIZEY = self.camera.altura
        offsety = SIZEY
        for depth in self.nodes_bd:
            n_hojas_vecinos = 0
            for node in depth:
                posY = offsety
                pos_init_father = 0
                if node.father is not None:
                    pos_init_father = node.father.box_init
                    n_hojas_hermanos = node.father.get_n_leaves_until(node)
                    n_hojas_vecinos = n_hojas_hermanos
                node.box_init = n_hojas_vecinos * SIZE + pos_init_father
                n_hojas_vecinos += node.get_n_leaves()
                posX = (node.get_n_leaves()*SIZE)/2 + node.box_init
                node.go_to((posX, posY))
            offsety += SIZEY


    def in_node(self, px: int, py: int) -> n.Node:
        """
        Obtiene el nodo que se encuentra en la posicion indicada.
        :param px:  Posicion en el eje X
        :param py:  Posicion en el eje Y
        :return:    Retorna el nodo que se encuentre en la posicion indicada
                    como parametro
        """
        for node in self.nodes:
            if node.in_body(px, py, self.camera):
                return node

    def get_max_father_index(self, node: n.Node) -> int:
        if node.father is None:
            return 0
        max_father_index = 0
        iter_node = node.father
        while iter_node is not None:
            index = self.nodes_bd[iter_node.depth-1].index(iter_node)
            max_father_index = max(index, max_father_index)
            iter_node = iter_node.father
        return max_father_index
