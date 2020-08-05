import math
import colorama

h, tau = 0.1, 0.05
xStart, xStop = 0, 1
tStart, tStop = 0, 0.5
n = int((xStop - xStart) / h)
m = int((tStop - tStart) / tau)
gamma = tau**2 / h**2

def fi(x):
	return (1-x**2) * math.cos(math.pi*x)
def psi(x):
	return 2*x + 0.6
def mu1(t):
	return  1 + 0.4*t
def mu2(t):
	return 0
def dk(i,k):
	return f'{i}|{k}'

U = {dk(i,0) : fi(h*i) for i in range(n+1)}
U.update({dk(0,k) : mu1(tau*k) for k in range(m+1)})
U.update({dk(n,k) : mu2(tau*k) for k in range(m+1)})

U.update({dk(i,1) : U[dk(i,0)] + tau*psi(h*i) + (tau**2 / 2) * (fi(h*(i+1)) 
		  - 2*fi(h*i) + fi(h*(i-1))) / h**2 for i in range(1,n)})

for k in range(1,m):
	for i in range(1,n):
		U[dk(i,k+1)] = 2*U[dk(i,k)] - U[dk(i,k-1)] + gamma*(U[dk(i+1,k)] 
			- 2*U[dk(i,k)] + U[dk(i-1,k)])

def table():
	colorama.init()
	
	def s(n=1): 
		return '█'*n
	def s2(n=8): 
		return '▒'*n

	cols = 15
	border = s(cols*8 - 2)

	caption1 = s() + s().join([str(i).center(8) for i in 
							  [s2(), 'x']+list(range(n+1))]) + s()
	caption2 = s() + s().join([str(i).center(8) for i in 
							  ['t', s2()]+[round(j*h,2) 
							  for j in range(m+1)]]) + s()

	print(colorama.Back.CYAN+border, caption1, border, caption2, sep='\n')

	lines = [] 
	for r in range(m+1):
		line = [round(r*tau,2), s2()] + [round(U[f'{i}|{r}'],4) 
				for i in range(n+1)]
		lines.append(s() + s().join([str(i).center(8) for i in line]) + s())

	for line in lines:
		print(colorama.Back.WHITE+border, line, sep='\n')

	print(border)

table()