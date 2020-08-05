from math import sin, cos, pi
import colorama

N, K = 13, 1
t, tau = 3, 0.1
omega = N*K
l1, l2, h1, h2 = 4, 3, 1, 1
gamma1, gamma2 = tau/h1**2, tau/h2**2

def key(i,j,k):
	return f'{i}|{j}|{k}'
def U(i,j,k):
	return Unodes[key(i,j,k)]

#Початкові умови
Unodes = {key(i,j,0) : N * sin(pi*(i*h1)/l1) * cos(pi*(j*h2)/l2)
		  for i in range(l1+1) for j in range(l2+1)}

#Граничні умови
Unodes.update({key(i,0,k) : 12 - 3*(h1*i)
			   for i in range(l1+1) for k in range(1,t+1)})
Unodes.update({key(i,l2,k) : 3*(h1*i) 
			   for i in range(l1+1) for k in range(1,t+1)})
Unodes.update({key(0,j,k) : 12 - 4*(h2*j) + N*sin(omega*k*tau) 
			   for j in range(l2+1) for k in range(1,t+1)})
Unodes.update({key(l1,j,k) : 4*(h2*j) + K*cos(omega*k*tau)
			   for j in range(l2+1) for k in range(1,t+1)})

#Граничні значення на півцілих часових шарах
Unodes.update({key(i,j,k+1/2) : (U(i,j,k+1) + U(i,j,k))/2 
			   - (tau*4) * ((U(i,j-1,k+1) - U(i,j-1,k) - 2*(U(i,j,k+1) 
			   - U(i,j,k)) + U(i,j+1,k+1) - U(i,j+1,k)) / h2**2) 
		   	   for j in range(1,l2) for k in range(t) for i in (0,l1)})

#Значення у внутрішніх вузлах
a1, b1, c1 = 0.5*gamma1, 0.5*gamma1, 1+gamma1
alpha1 = {key(1,j,k+1/2) : 0 for j in range(l2) for k in range(t)}
beta1 = {key(1,j,k+1/2) : U(0,j,k+1/2) for j in range(1,l2) 
		 for k in range(t)}

a2, b2, c2 = 0.5*gamma2, 0.5*gamma2, 1+gamma2
alpha2 = {key(i,1,k+1) : 0 for i in range(1,l1) for k in range(t)}
beta2 = {key(i,1,k+1) : U(i,0,k+1) for i in range(l1) for k in range(t)}

def F1(i,j,k):
	return U(i,j,k) + 0.5*tau*(U(i,j+1,k) -2*U(i,j,k) + U(i,j-1,k))/ h2**2
def F2(i,j,k):
	return U(i,j,k) + 0.5*tau*(U(i+1,j,k)-2*U(i,j,k)+U(i-1,j,k)) / h1**2

for k in range(t):
	for i in range(1,l1):
		for j in range(1,l2):
			alpha1[key(i+1,j,k+0.5)] = b1 / (c1 - a1*alpha1[key(i,j,k+0.5)])
			beta1[key(i+1,j,k+0.5)] = ((a1*beta1[key(i,j,k+0.5)] + F1(i,j,k)) 
				/ (c1 - a1*alpha1[key(i,j,k+0.5)]))

	for i in range(l1-1,0,-1):
		for j in range(1,l2):
			Unodes[key(i,j,k+0.5)] = (alpha1[key(i+1,j,k+0.5)]*U(i+1,j,k+0.5) 
				+ beta1[key(i+1,j,k+0.5)])

	for i in range(1,l1):
		for j in range(1,l2):
			alpha2[key(i,j+1,k+1)] = b2 / (c2 - a2*alpha2[key(i,j,k+1)])
			beta2[key(i,j+1,k+1)] = ((b2*beta2[key(i,j,k+1)] + F2(i,j,k+0.5)) 
				/ (c2 - a2*alpha2[key(i,j,k+1)]))

	for j in range(l2-1,0,-1):
		for i in range(1,l1):
			Unodes[key(i,j,k+1)] = (alpha2[key(i,j+1,k+1)]*U(i,j+1,k+1) 
				+ beta2[key(i,j+1,k+1)])

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
		line = [j*h2, s2()] + [round(U(i,j,k),5) for i in range(l1+1)]
		lines.append(s() + s().join([str(i).center(10) for i in line]) + s())

	for line in lines:
		print(colorama.Back.WHITE + border, line, sep='\n')

	print(border)

for k in range(t+1):
	print(colorama.Back.WHITE + f'\n{k} часовий шар')
	table(k)

