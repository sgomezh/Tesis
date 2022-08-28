import pygame
from node import Node
import node_manipulator

def main():
    raiz = Node([27, 27], [200, 200, 200], 1, 0)
    print(raiz)
    n_manipulator = node_manipulator.NodeManipulator(raiz)

    pygame.init()
    screen = pygame.display.set_mode((900, 500))
    pygame.display.set_caption("PyGraphicGraf")
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                n_manipulator.generate_son(x, y)

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            n_manipulator.camera.drag(0, 9)
        if pressed[pygame.K_s]:
            n_manipulator.camera.drag(0, -9)
        if pressed[pygame.K_d]:
            n_manipulator.camera.drag(-9, 0)
        if pressed[pygame.K_a]:
            n_manipulator.camera.drag(9, 0)
        if pressed[pygame.K_z]:
            n_manipulator.camera.anchura -= 1
            n_manipulator.update_position()
        if pressed[pygame.K_x]:
            n_manipulator.camera.anchura += 1
            n_manipulator.update_position()
        if pressed[pygame.K_f]:
            n_manipulator.camera.altura -= 1
            n_manipulator.update_position()
        if pressed[pygame.K_r]:
            n_manipulator.camera.altura += 1
            n_manipulator.update_position()

        n_manipulator.update()

        screen.fill((33, 33, 33))
        n_manipulator.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
