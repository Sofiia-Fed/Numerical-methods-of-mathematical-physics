import math
import colorama

n, m, s, k, l = 5, 3, 1, 13, 0.5
C, ro, lyambda = 0.427, 8900, 67.5
T1, T2 = k, 50*k
h = l / n
a1 = 1 / k
sigma = 1 / 6
a_kvadrat = lyambda / (C * ro)
tau = sigma * h**2 / a_kvadrat

def d(i,j=str()):
	return f'{i}{j}'

def K(i):
	return a_kvadrat*(1 + math.exp(-a1*i*h)) 

T = {d(0,i) : T1 for i in range(1,m+1)}
T.update({d(n,i) : T2 for i in range(1,m+1)})
T.update({d(i,0) : (T2-T1) / l**(s+1) * (i*h)**(s+1) + T1 
		 for i in range(n+1)})

a = {d(i) : tau * K(i-1/2) / h**2 for i in range(1,n)}
b = {d(i) : tau * K(i+1/2) / h**2 for i in range(1,n)}
c = {d(i) : (tau / h**2) * (K(i-1/2) + K(i+1/2)) + 1 
	 for i in range(1,n)}

alpha = {d(1) : 0}
beta = {d(1) : T1}

for k in range(1,m+1):
	for i in range(2,n+1):
		alpha[d(i)] = b[d(i-1)] / (c[d(i-1)] - alpha[d(i-1)]*a[d(i-1)])
		beta[d(i)] = ((a[d(i-1)]*beta[d(i-1)] + T[d(i-1,k-1)]) 
					  / (c[d(i-1)] - alpha[d(i-1)]*a[d(i-1)]))

	for i in range(4,0,-1):
		T[d(i,k)] = alpha[d(i+1)]*T[d(i+1,k)] + beta[d(i+1)]

#вивід таблиці в консоль
def table():
	colorama.init()
	
	def s(n=1): 
		return '█'*n
	def s2(n=10): 
		return '▒'*n

	cols = 8
	border = s(cols*11 + 1)

	caption1 = s() + s().join([str(i).center(10) for i in 
							  [s2(), 'i']+list(range(6))]) + s()
	caption2 = s() + s().join([str(i).center(10) for i in 
							  ['j', s2()]+[round(j*h,2) 
							  for j in range(6)]]) + s()

	print(colorama.Back.CYAN+border, caption1, border, caption2, sep='\n')

	lines = [] 
	for r in range(m+1):
		line = [r, s2()] + [round(T[f'{i}{r}'],3) for i in range(n+1)]
		lines.append(s() + s().join([str(i).center(10) for i in line]) + s())

	for line in lines:
		print(colorama.Back.WHITE+border, line, sep='\n')

	print(border)

table()
