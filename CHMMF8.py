from math import sin, cos, pi
import colorama

N, K = 13, 1
omega = N*K
l1, l2, h1, h2 = 4, 3, 1, 1
t, tau = 3, 0.1

gamma1, gamma2 = tau/h1**2, tau/h2**2

def dk(i,j,k):
	return f'{i}|{j}|{k}'

#Початкові умови
U = {dk(i,j,0) : N * sin(pi*(i*h1)/l1) * cos(pi*(j*h2)/l2)
		for i in range(l1+1) for j in range(l2+1)}

#Граничні умови
U.update({dk(i,0,k) : 12 - 3*(h1*i)
			for i in range(l1+1) for k in range(1,t+1)})
U.update({dk(i,l2,k) : 3*(h1*i) 
			for i in range(l1+1) for k in range(1,t+1)})
U.update({dk(0,j,k) : 12 - 4*(h2*j) + N*sin(omega*k*tau) 
			for j in range(l2+1) for k in range(1,t+1)})
U.update({dk(l1,j,k) : 4*(h2*j) + K*cos(omega*k*tau)
			for j in range(l2+1) for k in range(1,t+1)})

for k in range(0,t):
	for i in range(1,l1):
		for j in range(1,l2):
			U[dk(i,j,k+1)] = (U[dk(i,j,k)] 
				+ gamma1*(U[dk(i-1,j,k)] - 2*U[dk(i,j,k)] + U[dk(i+1,j,k)]) 
				+ gamma2*(U[dk(i,j-1,k)] - 2*U[dk(i,j,k)] + U[dk(i,j+1,k)]))

def table(k):
	colorama.init()

	def s(n=1): 
		return '█'*n
	def s2(n=10): 
		return '▒'*n

	cols = l1 + 3
	border = s(cols*11 + 1)

	caption1 = s() + s().join([str(i).center(10) 
							  for i in [s2(), 'x1'] + [j*h1 
							  for j in range(l1+1)]])
	caption1 += s()
	caption2 = s() + s().join([str(i).center(10) 
		for i in ['x2', s2()]+[s2() for j in range(l1+1)]])
	caption2 += s()

	print(colorama.Back.CYAN + border, caption1, border, caption2, sep='\n')

	lines = [] 
	for j in range(l2+1):
		line = [j*h2, s2()] + [round(U[dk(i,j,k)],5) for i in range(l1+1)]
		lines.append(s() + s().join([str(i).center(10) for i in line]) + s())

	for line in lines:
		print(colorama.Back.WHITE + border, line, sep='\n')

	print(border)

for k in range(t+1):
	print(colorama.Back.WHITE + f'\n{k} часовий шар')
	table(k)








