import os
import random
import pygame
import myconstants
from cortadora import Cortadora
from obstaculo import Obstaculo
from pasto import Pasto


# Iniciazlizar pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Configurar pantalla
pygame.display.set_caption("Get to the red square!")
pantalla = pygame.display.set_mode((320, 240))

fps = pygame.time.Clock()
obstaculos = [] # Contenedor de obstaculos
pastos = [] # Contenedor de pasto
cortadora = Cortadora() # Crear una cortadora


x = y = 0
for row in myconstants.ENTORNO1:
  for col in row:
    if col == "W":
        obstaculos.append(Obstaculo((x, y)))
    if col == "P":
        pastos.append(Pasto((x, y)))
    x += 16
  y += 16
  x = 0

running = True

while running:
  fps.tick(60)
  
  for e in pygame.event.get():
      if e.type == pygame.QUIT:
        running = False
      if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
        running = False
  
  # Mover de forma aleatoria
  cortadora.mover(obstaculos, pastos, pantalla)

  # Dibujar pantalla
  pantalla.fill((0, 0, 0))

  for obs in obstaculos:
    if obs.tocado == True:
      pygame.draw.rect(pantalla, (200, 100, 100), obs.rect)
    else:
      pygame.draw.rect(pantalla, (255, 255, 255), obs.rect)

  for pasto in pastos:
    if pasto.tocado == True:
      pygame.draw.rect(pantalla, (000, 255, 000), pasto.rect)
    else:
      pygame.draw.rect(pantalla, (000, 128, 000), pasto.rect)

  pygame.draw.rect(pantalla, (0, 96, 96), cortadora.rect)
  pygame.display.flip()

