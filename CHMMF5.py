import math
import colorama
n, m, l, h, a0, tau, k = 5, 3, 1, 0.2, 10, 1, 11

def d(i,j=str()):
	return f'{i}{j}'

def r(x, i=None):
	if i == '+':
		return 0.5 * (r(x) + abs(r(x)))
	elif i == '-':
		return 0.5 * (r(x) - abs(r(x)))
	else:
		return k * math.cos(math.pi * x)

def conditions(x):
	return a0 * (math.sin(k*x))**2

def mu(x):
	return 1 / (1 + 0.5*h*abs(r(x)))

T = {d(0,i) : a0 for i in range(m+1)}
T.update({d(n,i) : conditions(1) for i in range(m+1)})
T.update({d(i,0) : conditions(h*i) for i in range(1,n)})

a = {d(i) : mu(h*i)/h**2 - r(h*i,'-')/h for i in range(1,n)}
b = {d(i) : mu(h*i)/h**2 + r(h*i,'+')/h for i in range(1,n)}
c = {d(i) : 2*mu(h*i)/h**2 + 1/tau + r(h*i,'+')/h - r(h*i,'-')/h 
	 for i in range(1,n)}

alpha = {d(1) : 0}
beta = {}
for k in range(1,m+1):
	beta.update({d(1,k) : T[d(0,k)]})
	for i in range(2,n+1):
		alpha[d(i)] = b[d(i-1)] / (c[d(i-1)] - alpha[d(i-1)]*a[d(i-1)])
		beta[d(i,k)] = ((a[d(i-1)]*beta[d(i-1,k)] + T[d(i-1,k-1)]/tau) 
						/ (c[d(i-1)] - alpha[d(i-1)]*a[d(i-1)]))
	for i in range(4,0,-1):
		T[d(i,k)] = alpha[d(i+1)]*T[d(i+1,k)] + beta[d(i+1,k)]

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


