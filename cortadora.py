import pygame
from cuadrante import Cuadrante
from random import randint

class Cortadora(object):
    
  def __init__(self, mapa):
    self.busca_contorno = False
    self.tiene_posicion_inicial = False

    self.mapa = mapa # esto tiene eterno de prueba
    self.cuadrantes = []

    self.motor = False # esto sirve para pintar los pastos tocados
    self.velocidad = 2


    # si esta en false quiere decir q la cortadora se esta moviendo por lo tanto no busca
    # una nueva posicion
    self.buscar_nueva_pos = True
    
    # sirve para armar nuestro propio sistemas de cordenadas
    self.nueva_posicion_x = 0
    self.nueva_posicion_y = 0

    # sirve para armar tirar una posicion aleatoria en el entorno
    self.posicion_x = randint(1, 18)
    self.posicion_y = randint(1, 14)

    #elige un pasto al azar dentro del entorno
    lugar_inicial = mapa[self.posicion_y][self.posicion_x]
    x = lugar_inicial.rect.left
    y = lugar_inicial.rect.top

    self.posicion_destino_x = x
    self.posicion_destino_y = y

    self.rect = pygame.Rect(x, y, 16, 16)

  def mover(self):

    if self.rect.x != self.posicion_destino_x:

      if self.rect.x < self.posicion_destino_x:
        self.rect.x += self.velocidad
      else:
        self.rect.x -= self.velocidad

    if self.rect.y != self.posicion_destino_y:
      if self.rect.y < self.posicion_destino_y:
        self.rect.y += self.velocidad
      else:
        self.rect.y -= self.velocidad

    if self.rect.x == self.posicion_destino_x and self.rect.y == self.posicion_destino_y:
      self.buscar_nueva_pos = True

  #si tiene una nueva posicion hasta q no este en ese lugar no busque otra

  #Regla 1
  def detectar_posicion_inicial(self):
    if self.buscar_nueva_pos == True:
      self.buscar_nueva_pos = False

      if self.detectar_obstaculo("derecha") and self.detectar_obstaculo('abajo'):
        print "no moverse"
        self.tiene_posicion_inicial = True
        self.busca_contorno = True
        self.motor = True
        self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
        self.imprimir_cuadrantes()
      else:
        print "moverse"
        if self.detectar_obstaculo("derecha"):
          nueva_pos = self.moverse_abajo()
        else:
          nueva_pos = self.moverse_derecha()

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
    return self.hay_obstaculo(nueva_posicion)

  def detectar_abajo(self):
    nueva_posicion = self.mapa[self.posicion_y + 1][self.posicion_x]
    return self.hay_obstaculo(nueva_posicion)

  def detectar_izquierda(self):
    nueva_posicion = self.mapa[self.posicion_y][self.posicion_x - 1]
    return self.hay_obstaculo(nueva_posicion)

  def detectar_derecha(self):
    nueva_posicion = self.mapa[self.posicion_y][self.posicion_x + 1]
    return self.hay_obstaculo(nueva_posicion)

  def hay_obstaculo(self, posicion):
    if posicion.__class__.__name__ == "Obstaculo":
      return True
    else:
      return False

  def moverse_arriba(self):
    if self.tiene_posicion_inicial:
      self.nueva_posicion_y -= 1
    self.posicion_y -= 1
    return self.mapa[self.posicion_y][self.posicion_x]
  def moverse_abajo(self):
    if self.tiene_posicion_inicial:
      self.nueva_posicion_y += 1
    self.posicion_y += 1
    return self.mapa[self.posicion_y][self.posicion_x]
  def moverse_izquierda(self):
    if self.tiene_posicion_inicial:
      self.nueva_posicion_x -= 1
    self.posicion_x -= 1
    return self.mapa[self.posicion_y][self.posicion_x]
  def moverse_derecha(self):
    if self.tiene_posicion_inicial:
      self.nueva_posicion_x += 1
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
        self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
        self.imprimir_cuadrantes()
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

  def cargar_cuadrante(self, pos_x, pos_y):
    obs_arr = self.detectar_arriba()
    obs_aba = self.detectar_abajo()
    obs_izq = self.detectar_izquierda()
    obs_der = self.detectar_derecha()
    nuevo_cuandrante = Cuadrante(pos_x, pos_y, obs_arr, obs_aba, obs_izq, obs_der)
    self.cuadrantes.append(nuevo_cuandrante)

  def imprimir_cuadrantes(self):
    for i in range(0, len(self.cuadrantes)):
      print "Cuadrante %d:" % i
      print "Pos x: %d, Pos y: %d" %(self.cuadrantes[i].posicion_x, self.cuadrantes[i].posicion_y)
