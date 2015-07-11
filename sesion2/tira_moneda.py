import random

random.seed()

tries=1
bias=.5
coins=[]

for i in range(tries):
    n=random.random()
    if n < bias:
        coins.append('s')
    else:
        coins.append('a')

print coins[0]

