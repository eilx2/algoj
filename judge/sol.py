def calc(a):
	n=len(a)
	res = 0

	for i in range(n):
		res+=i*a[i]-(n-i-i)*a[i]

	return res

a = [int(x) for x in input().split()]
print(calc(a))