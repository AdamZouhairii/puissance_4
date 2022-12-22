import pygame
import  pyscroll
import pytmx

class Game :
    def __init__(self):
        self.screen= pygame.display.set_mode((600,600))
        pygame.display.set_caption('pokemon orange')
        img = pygame.image.load("icon.png")
        pygame.display.set_icon(img)
        tmx_data=pytmx.util_pygame.load_pygame('map1.tmx')
        map_data=pyscroll.data.TiledMapData(tmx_data)
        map_layer= pyscroll.orthographic.BufferedRenderer(map_data,self.screen.get_size())
        self.group= pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=5)

    def run(self):
        running=True
        while running:
            self.screen.blit(self.screen, (0,0))
            self.group.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.quit()