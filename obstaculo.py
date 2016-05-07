import pygame

class Obstaculo(object):
    
  def __init__(self, pos):
    self.tocado = False
    self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
