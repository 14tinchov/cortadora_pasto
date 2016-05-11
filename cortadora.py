import pygame
import time
from cuadrante import Cuadrante
from random import randint

class Cortadora(object):
    
  def __init__(self, mapa):
    self.busca_contorno = False
    self.tiene_posicion_inicial = False

    self.mapa = mapa # esto tiene entorno de prueba
    self.cuadrantes = []

    self.motor = False # esto sirve para pintar los pastos tocados
    self.velocidad = 1
    self.pausa = True


    # si esta en false quiere decir q la cortadora se esta moviendo por lo tanto no busca
    # una nueva posicion
    self.buscar_nueva_pos = True
    
    #Para completar la regla de la mano izquierda
    self.encontro_pared_derecha = False
    self.encontro_pared_izquierda = False
    self.encontro_pared_arriba = False
    self.encontro_pared_abajo = False

    # sirve para armar nuestro propio sistema de cordenadas
    self.nueva_posicion_x = 0
    self.nueva_posicion_y = 0

    self.x_inicial = 0
    self.y_inicial = 0
    self.posicion_actual_x = 0
    self.posicion_actual_y = 0

    self.cuadrante_analizado_abajo = False
    self.cuadrante_analizado_izquierda = False
    self.cuadrante_analizado_derecha = False
    self.cuadrante_analizado_arriba = False

    #Para hacer el recorrido interno
    self.x_minimo = 0
    self.x_maximo = 0
    self.y_minimo = 0
    self.y_maximo = 0

    # sirve para tirar una posicion aleatoria en el entorno
    self.posicion_x = randint(1, 18)
    self.posicion_y = randint(1, 14)

    #elige un pasto al azar dentro del entorno
    lugar_inicial = mapa[self.posicion_y][self.posicion_x]
    x = lugar_inicial.rect.left
    y = lugar_inicial.rect.top

    self.posicion_destino_x = x
    self.posicion_destino_y = y

    self.rect = pygame.Rect(x, y, 16, 16)

  def poner_pausa(self):
    if self.pausa == True:
      self.pausa = False
      time.sleep(2)

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
      if self.tiene_posicion_inicial == True:
        self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
        self.imprimir_cuadrantes()
      self.buscar_nueva_pos = True

  #si tiene una nueva posicion hasta q no este en ese lugar no busque otra

  #Regla 1
  def detectar_posicion_inicial(self):
    if self.buscar_nueva_pos == True:
      self.buscar_nueva_pos = False

      if self.detectar_obstaculo("derecha") and self.detectar_obstaculo('abajo'):
        #print "no moverse"
        self.tiene_posicion_inicial = True
        self.x_inicial = self.nueva_posicion_x
        self.y_inicial = self.nueva_posicion_y
        self.busca_contorno = True
        self.motor = True
      else:
        #print "moverse"
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
      self.posicion_actual_y -= 1
    self.posicion_y -= 1
    return self.mapa[self.posicion_y][self.posicion_x]
  def moverse_abajo(self):
    if self.tiene_posicion_inicial:
      self.nueva_posicion_y += 1
      self.posicion_actual_y += 1
    self.posicion_y += 1
    return self.mapa[self.posicion_y][self.posicion_x]
  def moverse_izquierda(self):
    if self.tiene_posicion_inicial:
      self.nueva_posicion_x -= 1
      self.posicion_actual_x -= 1
    self.posicion_x -= 1
    return self.mapa[self.posicion_y][self.posicion_x]
  def moverse_derecha(self):
    if self.tiene_posicion_inicial:
      self.nueva_posicion_x += 1
      self.posicion_actual_x += 1
    self.posicion_x += 1
    return self.mapa[self.posicion_y][self.posicion_x]


  def recorrer_contorno(self):
    if self.buscar_nueva_pos == True:
      self.buscar_nueva_pos = False    

      if self.detectar_obstaculo('derecha') == True and self.detectar_obstaculo('abajo') == False:
        #print "if abajo"
        nueva_pos = self.moverse_abajo()
        self.posicion_destino_y = nueva_pos.rect.top        
        self.analizar_cuadrante('abajo')        
        self.encontro_pared_derecha = True
        self.encontro_pared_arriba = False
        #self.comparar_coordenadas(self.posicion_actual_x,self.posicion_actual_y)
        self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
        return
      else:
        if self.detectar_obstaculo('derecha') == False  and self.encontro_pared_derecha == True:
          #print "else derecha"      
          nueva_pos = self.moverse_derecha()
          self.posicion_destino_x = nueva_pos.rect.left
          self.encontro_pared_derecha = False
          #self.comparar_coordenadas(self.posicion_actual_x,self.posicion_actual_y)
          self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
          return

      if self.detectar_obstaculo('abajo') == True  and self.detectar_obstaculo('izquierda') == False:
        #print "if izquierda"
        nueva_pos = self.moverse_izquierda()
        self.posicion_destino_x = nueva_pos.rect.left
        self.encontro_pared_abajo = True
        self.encontro_pared_derecha = False
        #self.comparar_coordenadas(self.posicion_actual_x,self.posicion_actual_y)
        self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
        #self.imprimir_cuadrantes()
        return
      else:
        if self.detectar_obstaculo('abajo') == False  and self.encontro_pared_abajo == True:
          #print "else abajo"      
          nueva_pos = self.moverse_abajo()
          self.posicion_destino_y = nueva_pos.rect.top
          self.encontro_pared_abajo = False
          #self.comparar_coordenadas(self.posicion_actual_x,self.posicion_actual_y)
          self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
          return

      if self.detectar_obstaculo('izquierda') == True  and self.detectar_obstaculo('arriba') == False:
        #print "if arriba"
        nueva_pos = self.moverse_arriba()
        self.posicion_destino_y = nueva_pos.rect.top
        self.encontro_pared_izquierda = True
        self.encontro_pared_abajo = False
        #self.comparar_coordenadas(self.posicion_actual_x,self.posicion_actual_y)
        self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
        return
      else:
        if self.detectar_obstaculo('izquierda') == False  and self.encontro_pared_izquierda == True:
          #print "else izquierda"      
          nueva_pos = self.moverse_izquierda()
          self.posicion_destino_x = nueva_pos.rect.left
          self.encontro_pared_izquierda = False
          #self.comparar_coordenadas(self.posicion_actual_x,self.posicion_actual_y)
          self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
          return

      if self.detectar_obstaculo('arriba') == True  and self.detectar_obstaculo('derecha') == False:
        #print "if derecha"      
        nueva_pos = self.moverse_derecha()
        self.posicion_destino_x = nueva_pos.rect.left
        self.encontro_pared_arriba = True
        self.encontro_pared_izquierda = False
        #self.comparar_coordenadas(self.posicion_actual_x,self.posicion_actual_y)
        self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
        return
      else:
        if self.detectar_obstaculo('arriba') == False  and self.encontro_pared_arriba == True:
          #print "else arriba"      
          nueva_pos = self.moverse_arriba()
          self.posicion_destino_y = nueva_pos.rect.top
          self.encontro_pared_arriba = False
          #self.comparar_coordenadas(self.posicion_actual_x,self.posicion_actual_y)
          self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
          return

  def cargar_cuadrante(self, pos_x, pos_y):
    obs_arr = self.detectar_arriba()
    obs_aba = self.detectar_abajo()
    obs_izq = self.detectar_izquierda()
    obs_der = self.detectar_derecha()
    nuevo_cuandrante = Cuadrante(pos_x, pos_y, obs_arr, obs_aba, obs_izq, obs_der)
    self.cuadrantes.append(nuevo_cuandrante)

  def imprimir_cuadrantes(self):
    pass
     #for i in range(0, len(self.cuadrantes)):

       #print "Cuadrante %d:" % i
       #print "Pos x: %d, Pos y: %d" %(self.cuadrantes[i].posicion_x, self.cuadrantes[i].posicion_y)

  def esta_en_posicion_inicial(self):
    if self.x_inicial == self.posicion_actual_x and self.y_inicial == self.posicion_actual_y:
      return True
    else:
      return False

  def analizar_cuadrante(self, direc):
    return {
        'abajo': self.analizar_abajo(),
        'arriba': self.analizar_arriba(),
        'izquierda': self.analizar_izquierda(),
        'derecha': self.analizar_derecha(),
    }[direc]

  def analizar_arriba(self):
    self.cuadrante_analizado_arriba = False
    for i in range(0, len(self.cuadrantes)):
      if self.cuadrantes[i].posicion_x == self.nueva_posicion_x and self.cuadrantes[i].posicion_y == self.nueva_posicion_y-1:
        print "analizado arriba"
        self.cuadrante_analizado_arriba = True
        return
      #else:
        #print "no analizado"
        #return
  def analizar_abajo(self):
    self.cuadrante_analizado_abajo = False
    for i in range(0, len(self.cuadrantes)):
      if self.cuadrantes[i].posicion_x == self.nueva_posicion_x and self.cuadrantes[i].posicion_y == self.nueva_posicion_y+1:
        print "analizado abajo"
        self.cuadrante_analizado_abajo = True
        return
      #else:
        #print self.cuadrante_analizado_abajo
        #return
  def analizar_derecha(self):
    self.cuadrante_analizado_derecha = False
    for i in range(0, len(self.cuadrantes)):
      if self.cuadrantes[i].posicion_x == self.nueva_posicion_x+1 and self.cuadrantes[i].posicion_y == self.nueva_posicion_y:
        print "analizado derecha"
        self.cuadrante_analizado_derecha = True
        return
      #else:
        #print "no analizado"
        #return
  def analizar_izquierda(self):
    self.cuadrante_analizado_izquierda = False
    for i in range(0, len(self.cuadrantes)):
      if self.cuadrantes[i].posicion_x == self.nueva_posicion_x-1 and self.cuadrantes[i].posicion_y == self.nueva_posicion_y:
        print "analizado izquierda"
        self.cuadrante_analizado_izquierda = True
        return
      #else:
        #print "no analizado"
        #return
      
  def recorrer_contorno_interno(self):
    self.analizar_cuadrante('izquierda')
    if self.cuadrante_analizado_izquierda == False:
        print "mover izquierda"
        nueva_pos = self.moverse_izquierda()
        self.posicion_destino_x = nueva_pos.rect.left
        #self.encontro_pared_abajo = True
        #self.encontro_pared_derecha = False
        #self.comparar_coordenadas(self.posicion_actual_x,self.posicion_actual_y)
        self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
        #self.imprimir_cuadrantes()
        return

    self.analizar_cuadrante('abajo')
    self.analizar_cuadrante('derecha')
    if self.cuadrante_analizado_abajo == True and self.cuadrante_analizado_derecha == True:
      print "mover izquierda"
      nueva_pos = self.moverse_izquierda()
      self.posicion_destino_x = nueva_pos.rect.left
      #self.encontro_pared_abajo = True
      #self.encontro_pared_derecha = False
      #self.comparar_coordenadas(self.posicion_actual_x,self.posicion_actual_y)
      self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
      #self.imprimir_cuadrantes()
      return

    self.analizar_cuadrante('izquierda')
    self.analizar_cuadrante('abajo')
    if self.cuadrante_analizado_abajo == True and self.cuadrante_analizado_derecha == True:
      print "mover arriba"
      nueva_pos = self.moverse_arriba()
      self.posicion_destino_y = nueva_pos.rect.top
      #self.encontro_pared_abajo = True
      #self.encontro_pared_derecha = False
      #self.comparar_coordenadas(self.posicion_actual_x,self.posicion_actual_y)
      self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
      #self.imprimir_cuadrantes()
      return

    self.analizar_cuadrante('izquierda')    
    self.analizar_cuadrante('arriba')
    if self.cuadrante_analizado_abajo == True and self.cuadrante_analizado_derecha == True:
      print "mover derecha"
      nueva_pos = self.moverse_derecha()
      self.posicion_destino_x = nueva_pos.rect.left
      #self.encontro_pared_abajo = True
      #self.encontro_pared_derecha = False
      #self.comparar_coordenadas(self.posicion_actual_x,self.posicion_actual_y)
      self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
      #self.imprimir_cuadrantes()
      return

    self.analizar_cuadrante('arriba')
    self.analizar_cuadrante('derecha')
    if self.cuadrante_analizado_abajo == True and self.cuadrante_analizado_derecha == True:
      print "mover abajo"
      nueva_pos = self.moverse_abajo()
      self.posicion_destino_y = nueva_pos.rect.top
      #self.encontro_pared_abajo = True
      #self.encontro_pared_derecha = False
      #self.comparar_coordenadas(self.posicion_actual_x,self.posicion_actual_y)
      self.cargar_cuadrante(self.nueva_posicion_x, self.nueva_posicion_y)
      #self.imprimir_cuadrantes()
      return
    

  def comparar_coordenadas(self, x, y):
    if self.x_minimo > x:
      self.x_minimo = x
    else:
      if self.x_maximo < x:
        self.x_maximo = x

    if self.y_minimo > y:
      self.y_minimo = y
    else:
      if self.y_maximo < y:
        self.y_maximo = y

    print "x_minimo %d x_maximo %d y_minimo %d y_maximo %d" %(self.x_minimo, self.x_maximo, self.y_minimo, self.y_maximo)

    


    
    