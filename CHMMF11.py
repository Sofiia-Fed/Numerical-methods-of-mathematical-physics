import sympy as sp
import numpy as np
m, n = 5, 4
nds = m*n
elmnts = 2*(n-1)*(m-1)

Nodes = {}
for i in range(1,nds+1):
	x = (i-1) % n
	y = m - 1 - (i-1)//n
	Nodes[i] = (x, y)

count = (i for i in range(1,n*(m-1)) if i%n)
Elements = {}
num = 0
for i in count:
	num += 1
	Elements[num] = sorted([i, i+n, i+n+1])
	num += 1
	Elements[num] = sorted([i, i+1, i+1+n], reverse=True)

def N(i,j,k):
	x, y = sp.var('x'), sp.var('y')
	alpha = Nodes[j][0]*Nodes[k][1] - Nodes[k][0]*Nodes[j][1]
	beta = Nodes[j][1] - Nodes[k][1]
	gamma = Nodes[k][0] - Nodes[j][0]
	return alpha + beta*x + gamma*y

def key(i,j,k=str()):
	return f'{i}|{j}|{k}'

N_ei = {}
for e in range(1,elmnts+1):
	i = Elements[e]
	N_ei[key(e,i[0])] = N(i[0], i[1], i[2])
	N_ei[key(e,i[1])] = N(i[1], i[2], i[0])
	N_ei[key(e,i[2])] = N(i[2], i[0], i[1])

def K(e,l,m):
	x, y = sp.var('x'), sp.var('y')
	if key(e,m,l) in K_elm:
		return K_elm[key(e,m,l)]
	else:
		deposit = sp.diff(N_ei[key(e,l)],x)*sp.diff(N_ei[key(e,m)],x)
		deposit += sp.diff(N_ei[key(e,l)],y)*sp.diff(N_ei[key(e,m)],y)
		return deposit

K_elm = {}
for e in range(1,elmnts+1):
	for l in Elements[e]:
		for s in Elements[e]:
			K_elm[key(e,l,s)] = K(e,l,s) 

U = {}
U.update({i : 150 for i in range(1,5)})
U.update({i : 114.75 for i in (5,8)})
U.update({i : 79.5 for i in (9,12)})
U.update({i : 44.25 for i in (13,16)})
U.update({i : 9 for i in range(17,21)})

GlobalMatrix = {}
for i in range(1, nds+1):
	for j in range(1, nds+1):
		for k in K_elm:
			if k.split('|')[1:] == [str(i), str(j)]:
				if key(i,j) not in GlobalMatrix:
					GlobalMatrix[key(i,j)] = K_elm[k]
				else:
					GlobalMatrix[key(i,j)] += K_elm[k]


unknown_vars = [i for i in range(1, nds+1) if 0 not in Nodes[i] and 
				Nodes[i][0]!=n-1 and Nodes[i][1]!=m-1]

A = []
for i in unknown_vars:
	A.append([])
	for j in unknown_vars:
		A[-1].append(GlobalMatrix[key(i,j)] if key(i,j) in GlobalMatrix else 0)

b = []
for i in unknown_vars:
	var = 0
	for k in GlobalMatrix:
		if int(k.split('|')[1]) == i:
			if int(k.split('|')[0]) not in unknown_vars:
				var += -GlobalMatrix[k]*U[int(k.split('|')[0])]
	b.append(var)

result = np.linalg.solve(np.array(A, dtype=float), np.array(b, dtype=float))
U.update({i : j for i,j in zip(unknown_vars,result)})

print('\nВузли:')
for i in range(1,m+1):
	for j in range(1,n+1):
		print(f'{n*(i-1)+j} : {Nodes[n*(i-1)+j]}'.center(15), end='')
	print()

print('\nСкінченні елементи:')
for i in range(1,m):
	for j in range(1,2*n-1):
		print(f'{2*(n-1)*(i-1)+j} : {Elements[2*(n-1)*(i-1)+j]}'.center(20), end='')
	print()

print(f'\nВузли з невідомими значеннями: {unknown_vars}')
print(f'Знайдені значення: {result}')

print('\nРезультат:')
for i in range(1,m+1):
	for j in range(1,n+1):
		print(f'{round(U[n*(i-1)+j],4)}'.center(10), end='')
	print()
print()




