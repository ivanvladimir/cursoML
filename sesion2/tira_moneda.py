import random

random.seed()

tries=100
bias=.8
coins=[]

for i in range(tries):
    n=random.random()
    print n
    if n < bias:
        coins.append('s')
    else:
        coins.append('a')

print coins

