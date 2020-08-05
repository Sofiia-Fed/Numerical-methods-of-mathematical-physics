import matplotlib.pyplot as plt
import colorama
n, m, k, s, l = 5, 3, 13.0, 1, 0.5
T1, T2 = k, 50*k
h = l/n

tau, C, ro, lyambda = 0.2, 0.427, 8900, 67.5
a_kvadrat = lyambda / (C * ro)
sgma = (a_kvadrat * tau) / h**2

T = {}
def t(i, j):
	return f'{i}{j}'

for i in range(1,m+1):
	T[t(0,i)] = T1
	T[t(n,i)] = T2 

for i in range(n+1):
	T[t(i,0)] = (T2-T1) / l**(s+1) * (i*h)**(s+1) + T1

for k in range(m+1):
	for i in range(1,5):
		T[t(i,k+1)] = (1 - 2*sgma)*T[t(i,k)] + sgma*(T[t(i-1,k)] + T[t(i+1, k)])

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
		line = [r, s2()] + [round(T[f'{i}{r}'],3) 
				for i in range(n+1)]
		lines.append(s() + s().join([str(i).center(10) 
				for i in line]) + s())

	for line in lines:
		print(colorama.Back.WHITE+border, line, sep='\n')
	print(border)

def plot():
	
	plt.figure(figsize=(15,3))

	for i in range(n+1):
		plt.subplot(131)
		plt.plot(list(range(1,m+2)), [T[t(i,j)] for j in range(m+1)])

	for i in range(m+1):
		plt.subplot(132)
		plt.plot(list(range(1,n+2)), [T[t(j,i)] for j in range(n+1)])

	plt.show()

table()
plot()







