import base64

input_data = base64.b64decode(input().encode()).decode()
judge_out = base64.b64decode(input().encode()).decode()
user_out = base64.b64decode(input().encode()).decode()

# begin judge here

judge_out = judge_out.split()
user_out = user_out.split()

if judge_out == user_out:
	print(1)
else:
	print(0)
