import sys


input_data = input()
judge_out = input().split()
user_out = input().split()


if judge_out == user_out:
	print(1)
else:
	print(0)
