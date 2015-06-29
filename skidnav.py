from FGAme import *
from FGAme.mathutils import convex_hull, pi
from random import normalvariate, uniform
from FGAme import signal
from math import *

###############################################################################
#                                 Autores
###############################################################################
#
# Nome/matrícula:Lucas Costa Araujo / 130060313
# Nome/matrícula:Lucas Gomes Pereira / 130013242
#
# 1) Criar o chao (OK!)
#
# 2) Criar las Personitas (OK!)
#    
# 3) Criar o tiro (  )
#    
# 4) Criar os inputs (  )
# 
# 5) Criar os indicadores de angulo (  )

###############################################################################
#                           Constantes do jogo
###############################################################################
WIDTH = 800
HEIGHT = 600
G = Vector(0,-20)
wind = Vector(-5,0)

###############################################################################
#                             Implementação
###############################################################################

class Player(Poly):

	@listen('collision')
	def handle_collision(self, col):
		other = col.other(self)
		if other.name == 'Floor':
			self.make_static()
			self.vel = Vector(0,0)
		else:
			pass

		

class Bullet(Poly):
	
	def __init__(self, pos, world):
		bullet_vertices = [(0,0),(25,0),(25,25),(0,25)]

		Poly.__init__(self, bullet_vertices, color='green', pos=pos, mass = '100', world = world)
		
		self.make_static()
		self.name = 'bullet'
		self.is_flying = 0 #variavel pode ser eliminada caso consiga voltar o objeto ao estado dinamico

	@listen('collision')
	def handle_collision(self, col):
		other = col.other(self)
		if other.name == 'Floor':
			self.make_static()
			self.vel = Vector(0,0)
		elif other.name == '1' or other.name == '2':
			print('Atingiu o player' + other.name)

		else:
			pass
		
class Power_bar(Poly):

	def __init__(self, pos, world):
		power_bar_vertices = [(0,0),(10,0),(10,50),(0,50)]

		Poly.__init__(self, power_bar_vertices, color='red', pos=pos, world = world)
		
		self.make_static()
		self.name = 'power'
		self.angle = 0
	pass

class Skidnav(World):
	"""Define o mundo do jogo Skidnav"""
	def __init__(self):
		World.__init__(self, background='white', gravity = 500, rest_coeff=0)

		#Cria chao
		floor_vertices = [(0, 0), (WIDTH, 0), (WIDTH, 100), (0,100)]
		self.floor = Poly(floor_vertices, color='black', pos=Vector(WIDTH/2,0), mass='inf', world=self)
		self.add(self.floor)
		self.floor.name = 'Floor'

		#Cria personagens
		player_vertices = [(0, 0),(25, 0),(25, 50),(0, 50)]
		self.player1 = Player(player_vertices, color='blue', pos=Vector(120,125), world = self)
		self.player2 = Player(player_vertices, color='red', pos=Vector(WIDTH-120,125), world = self)
		#self.player1.collision_signal = signal('collision')
		self.player1.name = '1'
		self.player2.name = '2'
		self.player2.vida = 100

		self.player1.bullet = 0
		self.player1.power_bar = 0
		self.player1.can_shoot = 1

		self.add(self.player1)
		self.add(self.player2)
		self.name = 'World'


	@listen('frame-enter')
	def init_frame(self):
		
		bullet = self.player1.bullet

		if self.player1.bullet != 0:

			if bullet.is_flying == 1:
				bullet.vel += G #Ja que o objeto nao eh dinamico temos que aplicar a fisica nele
				bullet.vel += wind

			if bullet.pos.y <= self.floor.ymax or bullet.pos.x > WIDTH:
				bullet.vel = Vector(0,0)
				self.player1.can_shoot = 1

			else: 
				bullet.rotate(0.2)
			
			# o normal seria WIDTH apenas... sem ser WIDTH/2 isso seria que outro projetil so pode ser
			# lançado ser lançado depois do primeiro sair da tela ou tocar o chao
			# para restringir atirar demais, nao sei se jogaremos por rodada... acho melhor nao
			# if bullet.pos.x > WIDTH/2 or bullet.pos.y > HEIGHT- 130:
			# 	self.player1.can_shoot = 1

	@listen('key-down', 'space')
	def start_power_bar(self):
		#cria a barra
		if self.player1.can_shoot == 1:
			self.player1.power_bar = Power_bar( pos=self.player1.pos - Vector(50,0), world = self)
			self.add(self.player1.power_bar)

			self.player1.bullet = Bullet( pos= self.player1.pos + Vector(50,0), world = self)
			self.add(self.player1.power_bar)

	@listen('long-press', 'space')
	def powering_shot(self):

		#if self.player1.can_shoot == 1:
		self.player1.power_bar.angle += 0.08
		self.player1.power_bar.pos.y += sin(self.player1.power_bar.angle)*5

	@listen('key-up', 'space')
	def end_power_bar(self):

		if self.player1.can_shoot == 1:
			print("released")
			#Removing power_bar from the world \o/
			# self.remove(self.player1.power_bar)
			power = self.player1.power_bar.pos.y 
			# o sin deixa com que o ponto mais alto da barra
			# nao seja o ponto mais forte
			# se pegarmos a altura da barra fica mais tranquilo de medir a força :D

			self.player1.power_bar.pos.y = 1000
			self.player1.bullet.vel = Vector(10,10)*power/2.5
			self.player1.bullet.is_flying = 1
			#self.player1.bullet.make_dynamic() # esse metodo esta certo porem ele ta dando erro
			# make_dynamic() eh o oposto de make_static() desse jeito ele tenta recuperar
			# a massa e outros atributos

		self.player1.can_shoot = 0


if __name__ == '__main__':
    game = Skidnav()
    game.run()
