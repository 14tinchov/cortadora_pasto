import pygame

class Cuadrante(object):
    
  def __init__(self, pos_x, pos_y, vec_arr, vec_aba, vec_izq, vec_der):
    self.posicion_x = pos_x
    self.posicion_y = pos_y
    self.obstaculo_arriba = vec_arr
    self.obstaculo_abajo = vec_aba
    self.obstaculo_izquierda = vec_izq
    self.obstaculo_derecha = vec_der