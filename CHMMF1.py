import math 
import colorama

n, m, E = 3, 4, 0.01

P = 1/2 * (math.cos(math.pi/n) + math.cos(math.pi/m))
W = 2 / (1 + math.sqrt(1 - P**2))

Tb = {
	'T01' : 44.25, 'T02' : 79.5, 'T03' : 114.75,
	'T10' : 9, 'T20' : 9,
	'T14' : 150, 'T24' : 150,
	'T31' : 44.25, 'T32' : 79.5, 'T33' : 114.75
}

iters = []
def T(i, j):
	return f'T{i}{j}'

iter0 = {}
iter0.update(Tb)
for i in range(1,n):
	for j in range(1,m):
		Uij_list = [iter0[T(i,0)], iter0[T(i,m)], 
					iter0[T(0,j)], iter0[T(n,j)]]
		iter0[T(i,j)] = 1/4 * sum(Uij_list)
iters.append(iter0)

while True:
	iterX = {}
	iterX.update(Tb)
	iterK = iters[-1]
	for i in range(1,n):
		for j in range(1,m):
			Uij_list = [iterX[T(i-1,j)], iterK[T(i+1, j)], 
						iterX[T(i, j-1)], iterK[T(i, j+1)]]
			iterX[T(i,j)] = W/4 * sum(Uij_list)
			iterX[T(i,j)] += (1-W)*iterK[T(i,j)]
	iters.append(iterX)

	eps = [abs(i-j) for i,j in zip(iters[-1].values(), iters[-2].values())]
	if max(eps) < 0.1:
		break

def table():
	colorama.init()
	
	def s(n=1): 
		return '█'*n

	cols = len(iter0.keys()) - len(Tb) + 1
	border = s(cols*11 + 1)

	caption = s() + s().join(['k'.center(10)] + 
		                     [T(i,j).center(10) for i in range(1,n) 
		                     for j in range(1,m)]) + s()

	lines = [s() + str(num).center(10) + s() + 
			 s().join([str(round(value,4)).center(10) 
			 for value in list(iterK.values())[10:]]) + 
			 s() for num, iterK in enumerate(iters)]

	print(colorama.Back.CYAN + border, caption, sep='\n')
	for line in lines: 
		print(colorama.Back.WHITE + border, line, sep='\n')
	print(border)

table()



