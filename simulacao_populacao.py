import simpy
from random import random as rand
import numpy as np

# Funcao de poisson: evento -> log(random)/tam_evento
def proximo_evento(evento):
	return -np.log(rand())/evento

class Population:
	def __init__(self, env, tempo_anos):
		self.population_per_age = np.array([16521114,17420159,17047159,
									 15017472,13564878,12638078,
									 11063493,9463763,7834714,
									 6124688,5165128,4242124,
									 3636858,2776060,1889918,
									 1290218,1129651])

		self.birth_list = np.array([23.58,23.02,22.58,
									22.24,21.99,21.8,
									21.62,21.44,21.2,
									20.89,20.48,19.97,
									19.39,18.75,18.08,
									17.43,16.84,16.33,
									15.91,15.59])

		self.death_rate = np.array([6.188686792,0.381167589,0.409745694,
									1.071019144,1.672333507,1.990888171,
									2.442718588,3.117575958,4.124464531,
									5.690085764,8.25420009,11.61658641,
									16.62149031,24.00164262,37.19526456,
									57.20738666,113.0278289])


		self.birth_rate = self.birth_list[0]
		self.time_duration = tempo_anos
		self.env = env
		self.birth_process = env.process(self.birth())
		self.death_process = [env.process(self.death(i)) for i in range(17)]
		self.update_process = env.process(self.update_age())

	def birth(self):
		yield self.env.timeout(proximo_evento(self.birth_rate))
		while self.env.now < self.time_duration:
			self.population_per_age[0] += 1000
			yield self.env.timeout(proximo_evento(self.birth_rate))

	def death(self,i):
		yield self.env.timeout(proximo_evento(self.death_rate[i]))
		while self.env.now < self.time_duration:
			self.population_per_age[i] -= 1000 if self.population_per_age[i] > 1000 else self.population_per_age[i]
			yield self.env.timeout(proximo_evento(self.death_rate[i]))

	def update_age(self):
		while self.env.now < self.time_duration:
			yield self.env.timeout(1)
			i = int(self.env.now)
			trans = self.population_per_age[:-1]/5
			self.population_per_age -= np.hstack((trans,[0]))
			self.population_per_age += np.hstack(([0],trans))
			self.birth_rate = self.birth_list[i]

			print "Census %d: " %(1991+i)
			print "Total: %d" %sum(self.population_per_age)
			print 'Distribuicao: ' + str(self.population_per_age)
			"""for i in range(len(self.population_per_age)):
				if i == 0:
					print "[0-5]: " + str(self.population_per_age[i])
				if i == len(self.population_per_age)-1:
					print "[81+]: " + str(self.population_per_age[i])
				else:
					print '[' + str(i*5+1) + '-' + str(i*5+5) + ']:' + str(self.population_per_age[i])
"""

env = simpy.Environment()
pop = Population(env,19)

env.run()
