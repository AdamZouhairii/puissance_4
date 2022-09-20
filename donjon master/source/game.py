import pygame
import pytmx
import pyscroll

from source.player import Player


class Game:
    def __int__(self):
        #cree la fenetre
        self.screen=pygame.display.set_mode((800,600))
        pygame.display.set_caption("donjon master")
        img = pygame.image.load("../image/icon.png")
        pygame.display.set_icon(img)

        tmx_data =pytmx.util_pygame.load_pygame("../monde/map.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer =pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())

        #genere joueur
        self.player = Player()


        #group calque
        self.group =pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
        self.group.add(self.player)

        running = True

        while running :

            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get() :
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()