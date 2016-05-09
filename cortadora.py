import pygame
from random import randint

class Cortadora(object):
    
  def __init__(self, mapa):
    self.mapa = mapa

    self.velocidad = 2
    self.tiene_posicion_inicial = False
    self.busca_contorno = False
    self.nuevo_destino = False
    self.buscar_nueva_pos = True
    
    self.posicion_inicial_x = 0
    self.posicion_inicial_y = 0

    self.posicion_x = randint(1, 18)
    self.posicion_y = randint(1, 14)

    

    #fila , columna
    lugar_inicial = mapa[self.posicion_y][self.posicion_x]

    x = lugar_inicial.rect.left
    y = lugar_inicial.rect.top

    self.posicion_destino_x = x
    self.posicion_destino_y = y

    self.rect = pygame.Rect(x, y, 16, 16)

  def mover(self):
    if self.rect.x != self.posicion_destino_x:
      # print "x:"
      # print "actual: %f" % self.rect.x
      # print "destino: %f" % self.posicion_destino_x
      if self.rect.x < self.posicion_destino_x:
        self.rect.x += 1
      else:
        self.rect.x -= 1
    if self.rect.y != self.posicion_destino_y:
      # print "y:"
      # print "actual: %f" % self.rect.y
      # print "destino: %f" % self.posicion_destino_y
      if self.rect.y < self.posicion_destino_y:
        self.rect.y += 1
      else:
        self.rect.y -= 1

    if self.rect.x == self.posicion_destino_x and self.rect.y == self.posicion_destino_y:
      self.buscar_nueva_pos = True

  #si tiene una nueva posicion hasta q no este en ese lugar no busque otra

  #Regla 1
  def detectar_posicion_inicial(self):
    if self.buscar_nueva_pos == True:
      self.buscar_nueva_pos = False
      nueva_pos = self.moverse_derecha()

      if self.detectar_obstaculo("derecha"):
        print "no moverse"
        self.tiene_posicion_inicial = True
        self.busca_contorno = True
        self.posicion_inicial_x = nueva_pos.rect.left
        self.posicion_inicial_y = nueva_pos.rect.top
      else:
        print "moverse"
        self.posicion_destino_x = nueva_pos.rect.left
        self.posicion_destino_y = nueva_pos.rect.top

  def detectar_obstaculo(self, direccion):
    return {
        'arriba': self.detectar_arriba(),
        'abajo': self.detectar_abajo(),
        'izquierda': self.detectar_izquierda(),
        'derecha': self.detectar_derecha(),
    }[direccion]

  def detectar_arriba(self):
    nueva_posicion = self.mapa[self.posicion_y - 1][self.posicion_x]
    return self.hay_pasto(nueva_posicion)

  def detectar_abajo(self):
    nueva_posicion = self.mapa[self.posicion_y + 1][self.posicion_x]
    return self.hay_pasto(nueva_posicion)

  def detectar_izquierda(self):
    nueva_posicion = self.mapa[self.posicion_y][self.posicion_x - 1]
    return self.hay_pasto(nueva_posicion)

  def detectar_derecha(self):
    nueva_posicion = self.mapa[self.posicion_y][self.posicion_x + 1]
    return self.hay_pasto(nueva_posicion)

  def hay_pasto(self, posicion):
    if posicion.__class__.__name__ == "Obstaculo":
      return True
    else:
      return False

  def moverse_arriba(self):
    self.posicion_y -= 1
    return self.mapa[self.posicion_y][self.posicion_x]
  def moverse_abajo(self):
    self.posicion_y += 1
    return self.mapa[self.posicion_y][self.posicion_x]
  def moverse_izquierda(self):
    self.posicion_x -= 1
    return self.mapa[self.posicion_y][self.posicion_x]
  def moverse_derecha(self):
    self.posicion_x += 1
    return self.mapa[self.posicion_y][self.posicion_x]


  def recorrer_contorno(self):
    if self.buscar_nueva_pos == True:
      self.buscar_nueva_pos = False

      if self.detectar_obstaculo('derecha') == True and self.detectar_obstaculo('abajo') == False:
        print "abajo"
        nueva_pos = self.moverse_abajo()
        self.posicion_destino_y = nueva_pos.rect.top
        return
      if self.detectar_obstaculo('abajo') == True  and self.detectar_obstaculo('izquierda') == False:
        print "izquierda"
        nueva_pos = self.moverse_izquierda()
        self.posicion_destino_x = nueva_pos.rect.left
        return
      if self.detectar_obstaculo('izquierda') == True  and self.detectar_obstaculo('arriba') == False:
        print "arriba"
        nueva_pos = self.moverse_arriba()
        self.posicion_destino_y = nueva_pos.rect.top
        return
      if self.detectar_obstaculo('arriba') == True  and self.detectar_obstaculo('derecha') == False:
        print "derecha"      
        nueva_pos = self.moverse_derecha()
        self.posicion_destino_x = nueva_pos.rect.left
        return


# abajo, izq, arriba, derecha