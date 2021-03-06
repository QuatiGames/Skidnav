from FGAme import *
from FGAme.mathutils import convex_hull, pi
from random import normalvariate, uniform
from FGAme import signal
from math import *
import random

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
# 3) Criar o tiro (OK!)
#    
# 4) Criar os inputs (OK!)
# 
# 5) Criar os indicadores de angulo (QUASE)

###############################################################################
#                           Constantes do jogo
###############################################################################
WIDTH = 800
HEIGHT = 600

NUMERO_PARTICULAS = 100

### a gravidade e o vento sao aceleracoes, mas do jeito que esta nao esta correto
### do jeito que esta agora elas sao velocidades constantes que aplicam na velocidade da bala
###
G = Vector(0,-20)

global wind
wind = Vector(-9,2)

global TIME 
TIME = 0

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
			other.life -= 10
			print('player' + other.name + ':')
			print(other.life)
			self.make_static()

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

		#Intencidades do vento
		self.wind_intencity = [5, 10, 15]
		self.wind_angle = (random.randrange(3141592) / 1000000) + 3.141592

		#Cria chao
		floor_vertices = [(0, 0), (WIDTH, 0), (WIDTH, 100), (0,100)]
		self.floor = Poly(floor_vertices, color='black', pos=Vector(WIDTH/2,0), mass='inf', world=self)
		self.add(self.floor)
		self.floor.name = 'Floor'

		#Preparando forma dos personagens
		player_vertices = [(0, 0),(25, 0),(25, 50),(0, 50)]

		#Particulas
		self.particles = []

		for x in range(0,NUMERO_PARTICULAS):	
			particle = Circle(radius=3, pos=Vector(random.randrange(WIDTH),random.randrange(HEIGHT)))
			particle.make_static()
			particle.name = "particle"

			self.particles.append(particle)
			pass

		self.add(self.particles)
		
		#Criando player1
		self.player1 = Player(player_vertices, color='blue', pos=Vector(120,110), world = self)
		self.player1.name = '1'
		self.player1.bullet = 0
		self.player1.power_bar = Power_bar(pos=Vector(0,1000), world = self)
		
		self.player1.can_shoot = 1
		self.player1.is_shotting = 0
		self.player1.shot_angle = 0.0
		self.player1.shot_direction = Vector(0,0)
		self.player1.life_number = 3
		self.player1.life = []

		for x in range(1,4):
			life = Circle(radius=20, pos=Vector(0 + (40*x) ,HEIGHT - 40), color='blue')
			life.make_static()
			self.player1.life.append(life)
			pass
		self.add(self.player1.life)

		#Criando player2
		self.player2 = Player(player_vertices, color='red', pos=Vector(WIDTH-120,110), world = self)
		self.player2.name = '2'
		self.player2.bullet = 0
		self.player2.power_bar = Power_bar(pos=Vector(0,1000), world = self)
		
		self.player2.can_shoot = 1
		self.player2.is_shotting = 0
		self.player2.shot_angle = 0.0
		self.player2.shot_direction = Vector(0,0)
		self.player2.life_number = 3
		self.player2.life = []

		for x in range(1,4):
			life = Circle(radius=20, pos=Vector(WIDTH - (40*x) ,HEIGHT - 40), color='red')
			life.make_static()
			self.player2.life.append(life)
			pass
		self.add(self.player2.life)	

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
		#Anda o tempo
		global TIME
		TIME += 1

		if self.player1.bullet != 0:
			# checar colisao da bala do player1 com o player2
			xmmax = max(self.player1.bullet.xmin, self.player2.xmin)
			xMmin = min(self.player1.bullet.xmax, self.player2.xmax)

			ymmax = max(self.player1.bullet.ymin, self.player2.ymin)
			yMmin = min(self.player1.bullet.ymax, self.player2.ymax)

			if xMmin >= xmmax  and  yMmin >= ymmax:
				print('player2:')
				print(self.player2.life)
				# remover bala
				self.player1.bullet.pos.y = 1000
				#diminui a vida do player2
				if self.player2.life_number >= 0:
					self.player2.life_number -= 1
					self.player2.life[self.player2.life_number].pos.y = 1000
					pass

		if self.player2.bullet != 0:
			# checar colisao da bala do player1 com o player2
			xmmax = max(self.player2.bullet.xmin, self.player1.xmin)
			xMmin = min(self.player2.bullet.xmax, self.player1.xmax)

			ymmax = max(self.player2.bullet.ymin, self.player1.ymin)
			yMmin = min(self.player2.bullet.ymax, self.player1.ymax)

			if xMmin >= xmmax  and  yMmin >= ymmax:
				print('player1:')
				print(self.player1.life)
				#remover bala
				self.player2.bullet.pos.y = 1000
				#diminui a vida do player1
				if self.player1.life_number >= 0:
					self.player1.life_number -= 1
					self.player1.life[self.player1.life_number].pos.y = 1000
					pass


		#Se tiver passado o tempo muda o vento
		if TIME > 600:
			global wind
			self.wind_angle = (random.randrange(3141592) / 1000000) + 3.141592
			vector = Vector(1,0) * random.choice(self.wind_intencity)

			# rotacionando posiçao do vento
			x = cos(self.wind_angle)*vector.x - sin(self.wind_angle)*vector.y
			y = sin(self.wind_angle)*vector.x + cos(self.wind_angle)*vector.y

			wind = Vector(x,y)

			print (self.wind_angle, vector)
			print(wind)
			
			TIME = 0
			pass

		#Move as particulas
		for x in range(0, NUMERO_PARTICULAS):
			self.particles[x].pos += wind
			if self.particles[x].pos.x > WIDTH:
				self.particles[x].pos.x = 0
			elif self.particles[x].pos.x < 0:
				self.particles[x].pos.x = WIDTH

			if self.particles[x].pos.y > HEIGHT:
				self.particles[x].pos.y = 0
			elif self.particles[x].pos.y < 0:
				self.particles[x].pos.y = HEIGHT

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
		bullet2 = self.player2.bullet

		if bullet2 != 0:

			if bullet2.is_flying == 1:
				bullet2.vel += G #Ja que o objeto nao eh dinamico temos que aplicar a fisica nele
				bullet2.vel += wind

			if bullet2.pos.y <= self.floor.ymax or bullet2.pos.x > WIDTH or bullet2.pos.x < 0:
				# parando a bala
				bullet2.vel = Vector(0,0)
				self.player2.can_shoot = 1

			else: 
				bullet2.rotate(0.2)


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
		self.player1.bullet.vel = Vector(0,0.12)

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

		if player1.is_shotting == 1 and player1.shot_angle > 0.0:
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
		self.player2.bullet.vel = Vector(0,0.12)

	@listen('key-up', 'space')
	def end_power_bar2(self):

		if self.player2.can_shoot == 1:
			print("released")
			#Removing power_bar from the world \o/
			# self.remove(self.player2.power_bar)

			# Lançando bala
			power = self.player2.power_bar.power_line.pos.y
			self.player2.shot_direction =    self.player2.bullet.pos - self.player2.pos
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
			vector = self.player1.pos + Vector(50,0) 

			# rotacionando posiçao
			x = -cos(angle)*vector.x + sin(angle)*vector.y + WIDTH
			y = sin(angle)*vector.x + cos(angle)*vector.y

			# atualizando posiçao da bala
			player2.bullet.pos = Vector(x,y)
			print(player2.bullet.pos)

	@listen('long-press', 's')
	def low_angle_shot2(self):

		player2 = self.player2

		if player2.is_shotting == 1 and player2.shot_angle >= 0.0:
			player2.shot_angle -= 0.01
			print(player2.shot_angle)
			
			angle = player2.shot_angle
			vector = self.player1.pos + Vector(50,0)

			# Rotacionando posiçao 
			x = -cos(angle)*vector.x + sin(angle)*vector.y + WIDTH
			y = sin(angle)*vector.x + cos(angle)*vector.y

			# Atualizando posiçao da bala
			player2.bullet.pos = Vector(x,y)


if __name__ == '__main__':
    game = Skidnav()
    game.run()
