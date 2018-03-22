a=[]

def visit(node):
	if node==None:
		return

	visit(node.left)
	a.append(node.value)
	visit(node.right)


def linearize(node):
	visit(node)

	return a
