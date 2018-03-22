import random

class Tree:
	def __init__(self,l,r,value):
		self.value=value
		self.left=l
		self.right=r


n,maxv=[int(x) for x in input().split()]


a=[0]*n

for i in range(n):
	a[i]=random.randint(0,maxv)

a=sorted(a)


def rand(l,r):
	return random.randint(l,r)

f=open("input.txt","w")

root = rand(0,n-1)
f.write("{0}\n{1}\n".format(n,root))

adj=[(-1,-1)]*n

def get_tree(x,l,r):
	left=-1
	right=-1

	print(x)
	if x>l:
		left=rand(l,x-1)

	if x<r:
		right=rand(x+1,r)

	adj[x]=(left,right)
	if left!=-1: get_tree(left,l,x-1)
	if right!=-1: get_tree(right,x+1,r)
	

get_tree(root,0,n-1)

for i in range(n):
	f.write("{} {} {}\n".format(a[i],adj[i][0],adj[i][1]))


f.close()

	



