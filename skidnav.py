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
	
	@listen('collision')
	def handle_collision(self, col):
		other = col.other(self)
		if other.name == 'Floor':
			self.make_static()
			self.vel = Vector(0,0)
		elif other.name == '1' | other.name == '2':
			pass

		else:
			pass
		
class Power_bar(Poly):

	# def __init__(self, player1, world):
	# 	power_bar_vertices = [(0,0),(10,0),(10,50),(0,50)]

	# 	Poly.__init__(power_bar_vertices, color='red', pos=player1.pos - Vector(50,0), world = world)
		
		# power_bar.make_static()
		# power_bar.name = 'power'
		# power_bar.angle = 0
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

		self.add(self.player1)
		self.add(self.player2)
		self.name = 'World'


	@listen('frame-enter')
	def init_frame(self):
		pass

	@listen('key-down', 'space')
	def start_power_bar(self):
		#cria a barra
		
		power_bar_vertices = [(0,0),(10,0),(10,50),(0,50)]

		self.player1.power_bar = Power_bar(power_bar_vertices, color='red', pos=self.player1.pos - Vector(50,0), world = self)
		self.player1.power_bar.name = 'power'
		self.player1.power_bar.angle = 0
		self.player1.power_bar.make_static()
		self.add(self.player1.power_bar)

	@listen('long-press', 'space')
	def powering_shot(self):
		self.player1.power_bar.angle += 0.1
		self.player1.power_bar.pos.y += sin(self.player1.power_bar.angle)*10

	@listen('key-up', 'space')
	def end_power_bar(self):
		print("released")
		# self.remove(self.player1.power_bar)
		self.player1.power_bar.vel = Vector(0,500)

if __name__ == '__main__':
    game = Skidnav()
    game.run()
