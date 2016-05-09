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
mapa = []



aux = 0
x = y = 0

for row in myconstants.ENTORNO2:
  mapa.append([])
  for col in row:
    if col == "W":
      mapa[aux].append(Obstaculo((x, y)))
      obstaculos.append(Obstaculo((x, y)))
    if col == "P":
      mapa[aux].append(Pasto((x, y)))
      pastos.append(Pasto((x, y)))
    x += 16

  y += 16
  x = 0
  aux +=1

running = True

cortadora = Cortadora(mapa) # Crear una cortadora

while running:
  fps.tick(60)
  
  for e in pygame.event.get():
      if e.type == pygame.QUIT:
        running = False
      if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
        running = False
  
  # Mover de forma aleatoria
  # cortadora.mover(obstaculos, pastos, pantalla)
  if cortadora.busca_contorno == True:
    cortadora.recorrer_contorno()

  if cortadora.tiene_posicion_inicial == False:
    cortadora.detectar_posicion_inicial()


  cortadora.mover()

  # Dibujar pantalla
  pantalla.fill((0, 0, 0))

  for obs in obstaculos:
    if cortadora.rect.colliderect(obs.rect) and cortadora.motor == True:
      obs.tocado = True

    if obs.tocado == True:
      pygame.draw.rect(pantalla, (200, 100, 100), obs.rect)
    else:
      pygame.draw.rect(pantalla, (255, 255, 255), obs.rect)

  for pasto in pastos:
    if pasto.rect.colliderect(cortadora.rect) and pasto.tocado == False  and cortadora.motor == True:
      pasto.tocado = True

    if pasto.tocado == True:
      pygame.draw.rect(pantalla, (000, 255, 000), pasto.rect)
    else:
      pygame.draw.rect(pantalla, (000, 128, 000), pasto.rect)

  pygame.draw.rect(pantalla, (0, 96, 96), cortadora.rect)
  pygame.display.flip()
