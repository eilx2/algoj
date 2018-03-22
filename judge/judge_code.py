import sys
import sol
import traceback

input_file=sys.argv[1]
input_data = None

class Tree:
	def __init__(self,l,r,value):
		self.value=value
		self.left=l
		self.right=r

n=0
root=0
nodes=[]

with open(input_file,"r") as f:
	n=int(f.readline())
	root=int(f.readline())

	for i in range(n):
		nodes.append(Tree(None,None,0))

	for i in range(n):
		val,l,r=[int(x) for x in f.readline().split()]

		nodes[i].value=val

		nodes[i].left=None
		nodes[i].right=None

		if l!=-1:
			nodes[i].left=nodes[l]

		if r!=-1:
			nodes[i].right=nodes[r]


res=sol.linearize(nodes[root])

for x in res:
	print(x,end=' ')







