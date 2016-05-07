import pygame
from random import randint

class Cortadora(object):
    
  def __init__(self):
    self.rect = pygame.Rect(16, 16, 16, 16)
    self.direccion = (2, 0)
    self.direcciones = [
      (-2, 0), # Izquierda
      (2, 0),  # Derecha
      (0,-2),  # Abajo
      (0, 2)   # Arriba
    ]


  def mover(self, obstaculos, pastos, pantalla):
    dx, dy = self.direccion
    if dx != 0:
        self.mover_un_eje(dx, 0, obstaculos, pastos, pantalla)
    if dy != 0:
        self.mover_un_eje(0, dy, obstaculos, pastos, pantalla)

  def mover_un_eje(self, dx, dy, obstaculos, pastos, pantalla):
    # Mover cortadora
    self.rect.x += dx
    self.rect.y += dy

    # self.direccion = self.direcciones[randint(0, 3)]
    # Se mueve en base a la velocidad
    for obs in obstaculos:
      if self.rect.colliderect(obs.rect):
        obs.tocado = True
        self.direccion = self.direcciones[randint(0, 3)]
        if dx > 0: # Si choca con algo a la derecha, no se mueve
            self.rect.right = obs.rect.left
        if dx < 0: # Si choca con algo a la izquierda, no se mueve
            self.rect.left = obs.rect.right
        if dy > 0: # Si choca con algo a abajo, no se mueve
            self.rect.bottom = obs.rect.top
        if dy < 0: # Si choca con algo a arriba, no se mueve
            self.rect.top = obs.rect.bottom
    for pasto in pastos:
      if pasto.rect.colliderect(self.rect) and pasto.tocado == False:
        pasto.tocado = True
        self.direccion = self.direcciones[randint(0, 3)]
        if self.rect.left == pasto.rect.right:
          self.direccion = self.direcciones[1]
        if self.rect.right == pasto.rect.left:
          self.direccion = self.direcciones[0]
        if self.rect.bottom == pasto.rect.top:
          self.direccion = self.direcciones[3]
        if self.rect.top == pasto.rect.bottom:
          self.direccion = self.direcciones[2]

