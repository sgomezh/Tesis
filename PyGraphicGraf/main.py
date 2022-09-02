import pygame
from node import Node
import node_manipulator

def main():
    X_DIM = 1290
    Y_DIM = 900
    raiz = Node([27, 27], [200, 200, 200], 1, 0)
    print(raiz)
    n_manipulator = node_manipulator.NodeManipulator(raiz)

    pygame.init()
    screen = pygame.display.set_mode((X_DIM, Y_DIM), pygame.SRCALPHA, 320)
    pygame.display.set_caption("BART tree plotter")
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
            n_manipulator.camera.drag(0, 1)
        if pressed[pygame.K_s]:
            n_manipulator.camera.drag(0, -1)
        if pressed[pygame.K_d]:
            n_manipulator.camera.drag(-1, 0)
        if pressed[pygame.K_a]:
            n_manipulator.camera.drag(1, 0)
        if pressed[pygame.K_z]:
            n_manipulator.camera.anchura -= 0.25
            n_manipulator.update_position()
        if pressed[pygame.K_x]:
            n_manipulator.camera.anchura += 0.25
            n_manipulator.update_position()
        if pressed[pygame.K_q]:
            n_manipulator.camera.altura -= 0.25
            n_manipulator.update_position()
        if pressed[pygame.K_e]:
            n_manipulator.camera.altura += 0.25
            n_manipulator.update_position()

        n_manipulator.update()

        screen.fill((33, 33, 33))
        n_manipulator.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
