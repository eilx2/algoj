def count_in_array(A,x):
	cnt = 0
    for val in A:
    	if val==x:
    		cnt+=1

    return cnt


A = [int(v) for v in input().split()]
x = int(input())
print(count_in_array(A,x))