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
# 3) Criar o tiro (OK)
#    
# 4) Criar os inputs (OK)
# 
# 5) Criar os indicadores de angulo (QUASE)

###############################################################################
#                           Constantes do jogo
###############################################################################
WIDTH = 800
HEIGHT = 600

### a gravidade e o vento sao aceleracoes, mas do jeito que esta nao esta correto
### do jeito que esta agora elas sao velocidades constantes que aplicam na velocidade da bala
###
G = Vector(0,-20)
wind = Vector(-9,2)

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
		self.mass = '100'
		self.is_flying = 0 #variavel pode ser eliminada caso consiga voltar o objeto ao estado dinamico

	@listen('collision')
	def handle_collision(self, col):
		other = col.other(self)
		if other.name == 'Floor':
			self.make_static()
			self.vel = Vector(0,0)
			print('Colidiu com o chao')
		elif other.name == '1' or other.name == '2':
			print('Atingiu o player' + other.name)

		else:
			pass
		
class Power_bar(Poly):
	def __init__(self, pos, world):
		power_bar_vertices = [(0,0),(10,0),(10,50),(0,50)]

		Poly.__init__(self, power_bar_vertices, color='red', pos=pos, world=world)
		
		self.make_static()
		self.name = 'power'
		self.angle = 0

		#A linha q marca o forca do tiro
		line_vertices = [(0,0),(15,0),(15,5),(0,5)]
		self.power_line = Poly(line_vertices, color='white', pos=pos, world=world)
		self.power_line.name = 'line'
		self.power_line.angle = 0
		self.power_line.make_static()

class Skidnav(World):
	"""Define o mundo do jogo Skidnav"""
	def __init__(self):
		World.__init__(self, background='white', gravity = 500, rest_coeff=0)

		#Cria chao
		floor_vertices = [(0, 0), (WIDTH, 0), (WIDTH, 100), (0,100)]
		self.floor = Poly(floor_vertices, color='black', pos=Vector(WIDTH/2,0), mass='inf', world=self)
		self.add(self.floor)
		self.floor.name = 'Floor'

		#Preparando forma dos personagens
		player_vertices = [(0, 0),(25, 0),(25, 50),(0, 50)]
		
		
		#Criando player1
		self.player1 = Player(player_vertices, color='blue', pos=Vector(120,125), world = self)
		self.player1.name = '1'
		self.player1.bullet = 0
		self.player1.power_bar = Power_bar( pos=Vector(0,1000), world = self)
		
		self.player1.can_shoot = 1
		self.player1.is_shotting = 0
		self.player1.shot_angle = 0.0
		self.player1.shot_direction = Vector(0,0)

		#Criando player2
		self.player2 = Player(player_vertices, color='red', pos=Vector(WIDTH-120,125), world = self)
		self.player2.name = '2'
		self.player2.bullet = 0
		self.player2.power_bar = Power_bar( pos=Vector(0,1000), world = self)
		
		self.player2.can_shoot = 1
		self.player2.is_shotting = 0
		self.player2.shot_angle = 0.0
		self.player2.shot_direction = Vector(0,0)


		# adicionando player1 e relacionados ao mundo
		self.add(self.player1)
		self.add(self.player1.power_bar)
		self.add(self.player1.power_bar.power_line)

		# adicionando player2 e relacionados ao mundo
		self.add(self.player2)
		self.add(self.player2.power_bar)
		self.add(self.player2.power_bar.power_line)

		self.name = 'World'


	@listen('frame-enter')
	def init_frame(self):
		
		#Para o player 1
		bullet = self.player1.bullet

		if self.player1.bullet != 0:

			if bullet.is_flying == 1:
				bullet.vel += G #Ja que o objeto nao eh dinamico temos que aplicar a fisica nele
				bullet.vel += wind

			if bullet.pos.y <= self.floor.ymax or bullet.pos.x > WIDTH or bullet.pos.x < 0:
				# parando a bala
				bullet.vel = Vector(0,0)
				self.player1.can_shoot = 1

			else: 
				bullet.rotate(0.2)

		#para o player 2
		bullet = self.player2.bullet

		if bullet != 0:

			if bullet.is_flying == 1:
				bullet.vel += G #Ja que o objeto nao eh dinamico temos que aplicar a fisica nele
				bullet.vel += wind

			if bullet.pos.y <= self.floor.ymax or bullet.pos.x > WIDTH or bullet.pos.x < 0:
				# parando a bala
				bullet.vel = Vector(0,0)
				self.player1.can_shoot = 1

			else: 
				bullet.rotate(0.2)
			
			# o normal seria WIDTH apenas... sem ser WIDTH/2 isso seria que outro projetil so pode ser
			# lançado ser lançado depois do primeiro sair da tela ou tocar o chao
			# para restringir atirar demais, nao sei se jogaremos por rodada... acho melhor nao
			# if bullet.pos.x > WIDTH/2 or bullet.pos.y > HEIGHT- 130:
			# 	self.player1.can_shoot = 1


### Comandos para o player 1
	@listen('key-down', 'l')
	def start_power_bar(self):

		#Para o player 1
		#cria a barra
		self.player1.is_shotting = 1

		if self.player1.can_shoot == 1:
			# Voltando a barra de ppoder para a posicao certa
			self.player1.power_bar.pos = self.player1.pos - Vector(50,0)
			self.player1.power_bar.power_line.pos = self.player1.pos - Vector(50,0)

			# Criando bala
			self.player1.bullet = Bullet( pos= self.player1.pos + Vector(50,0), world = self)
			self.player1.bullet.make_static()


	@listen('long-press', 'l')
	def powering_shot(self):

		# Para o player1
		# atualizando angulo
		self.player1.power_bar.power_line.angle += 0.05

		# preparando variaveis
		bar_y_pos = self.player1.power_bar.pos.y
		cos_angle = cos(self.player1.power_bar.power_line.angle)
		bar_height = (self.player1.power_bar.height)

		# atualizando posiçao da power_line
		self.player1.power_bar.power_line.pos.y = -cos_angle*(bar_height/2) + bar_y_pos
		

	@listen('key-up', 'l')
	def end_power_bar(self):

		if self.player1.can_shoot == 1:
			print("released")
			#Removing power_bar from the world \o/
			# self.remove(self.player1.power_bar)

			# Lançando bala
			power = self.player1.power_bar.power_line.pos.y
			self.player1.shot_direction =  self.player1.bullet.pos - self.player1.pos 
			self.player1.bullet.vel = self.player1.shot_direction*power/4

			# removendo power bar
			self.player1.power_bar.pos.y = 1000
			self.player1.power_bar.power_line.pos.y = 1000
			self.player1.power_bar.power_line.angle = 0

			# atualizando bandeiras de combate
			self.player1.bullet.is_flying = 1
			self.player1.is_shotting = 0
			self.player1.shot_angle = 0.0
			
			#self.player1.bullet.make_dynamic() # esse metodo esta certo porem ele ta dando erro
			# make_dynamic() eh o oposto de make_static() desse jeito ele tenta recuperar
			# a massa e outros atributos

		self.player1.can_shoot = 0

	@listen('long-press', 'up')
	def grow_angle_shot(self):

		player1 = self.player1

		if player1.is_shotting == 1 and player1.shot_angle < 0.4:
			player1.shot_angle += 0.01

			angle = player1.shot_angle
			vector = self.player1.pos + Vector(50,0)

			# rotacionando posiçao
			x = cos(angle)*vector.x - sin(angle)*vector.y
			y = sin(angle)*vector.x + cos(angle)*vector.y

			# atualizando posiçao da bala
			player1.bullet.pos = Vector(x,y)

	@listen('long-press', 'down')
	def low_angle_shot(self):

		player1 = self.player1

		if player1.is_shotting == 1 and player1.shot_angle > 0.1:
			player1.shot_angle -= 0.01
			
			angle = player1.shot_angle
			vector = self.player1.pos + Vector(50,0)

			# Rotacionando posiçao 
			x = cos(angle)*vector.x - sin(angle)*vector.y
			y = sin(angle)*vector.x + cos(angle)*vector.y

			# Atualizando posiçao da bala
			player1.bullet.pos = Vector(x,y)

### Comandos para o player 2
	@listen('key-down', 'space')
	def start_power_bar2(self):

		#cria a barra
		self.player2.is_shotting = 1

		if self.player2.can_shoot == 1:
			# Voltando a barra de ppoder para a posicao certa
			self.player2.power_bar.pos = self.player2.pos + Vector(50,0)
			self.player2.power_bar.power_line.pos = self.player2.pos + Vector(50,0)

			# Criando bala
			self.player2.bullet = Bullet( pos= self.player2.pos - Vector(50,0), world = self)
			self.player2.bullet.make_static()


	@listen('long-press', 'space')
	def powering_shot2(self):

		# atualizando angulo
		self.player2.power_bar.power_line.angle -= 0.05

		# preparando variaveis
		bar_y_pos = self.player2.power_bar.pos.y
		cos_angle = cos(self.player2.power_bar.power_line.angle)
		bar_height = (self.player2.power_bar.height)

		# atualizando posiçao da power_line
		self.player2.power_bar.power_line.pos.y = -cos_angle*(bar_height/2) + bar_y_pos
		

	@listen('key-up', 'space')
	def end_power_bar2(self):

		if self.player2.can_shoot == 1:
			print("released")
			#Removing power_bar from the world \o/
			# self.remove(self.player2.power_bar)

			# Lançando bala
			power = self.player2.power_bar.power_line.pos.y
			self.player2.shot_direction =  self.player2.bullet.pos - self.player2.pos 
			self.player2.bullet.vel = self.player2.shot_direction*power/4

			# removendo power bar
			self.player2.power_bar.pos.y = 1000
			self.player2.power_bar.power_line.pos.y = 1000
			self.player2.power_bar.power_line.angle = 0

			# atualizando bandeiras de combate
			self.player2.bullet.is_flying = 1
			self.player2.is_shotting = 0
			self.player2.shot_angle = 0.0
			
			#self.player2.bullet.make_dynamic() # esse metodo esta certo porem ele ta dando erro
			# make_dynamic() eh o oposto de make_static() desse jeito ele tenta recuperar
			# a massa e outros atributos

		self.player2.can_shoot = 0

	@listen('long-press', 'w')
	def grow_angle_shot2(self):

		player2 = self.player2

		if player2.is_shotting == 1 and player2.shot_angle < 0.4:
			player2.shot_angle += 0.01

			angle = player2.shot_angle
			vector = self.player2.pos + Vector(50,0)

			# rotacionando posiçao
			x = cos(angle)*vector.x - sin(angle)*vector.y
			y = sin(angle)*vector.x + cos(angle)*vector.y

			# atualizando posiçao da bala
			player2.bullet.pos = Vector(x,y)

	@listen('long-press', 's')
	def low_angle_shot2(self):

		player2 = self.player2

		if player2.is_shotting == 1 and player2.shot_angle > 0.1:
			player2.shot_angle -= 0.01
			
			angle = player2.shot_angle
			vector = self.player2.pos + Vector(50,0)

			# Rotacionando posiçao 
			x = cos(angle)*vector.x - sin(angle)*vector.y
			y = sin(angle)*vector.x + cos(angle)*vector.y

			# Atualizando posiçao da bala
			player2.bullet.pos = Vector(x,y)


if __name__ == '__main__':
    game = Skidnav()
    game.run()
