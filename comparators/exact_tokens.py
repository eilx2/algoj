import base64
import sys

input_data = base64.b64decode(input().encode()).decode()
judge_out = base64.b64decode(input().encode()).decode()

try:
	user_out = base64.b64decode(input().encode()).decode()
except:
	print(0)
	sys.exit()

# begin judge here

judge_out = judge_out.split()
user_out = user_out.split()

if judge_out == user_out:
	print(1)
else:
	print(0)
