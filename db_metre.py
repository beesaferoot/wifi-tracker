import math
def sol(signalDB,freqMHZ):
	result=(27.55-(20*math.log10(freqMHZ)+signalDB))/20
	return 10**result

if __name__ =="__main__":
	tt=int(input())
	for i in range(tt):
		a,b=list(map(float, input().split()))
		print("Case #{}: {}m".format(i+1,sol(a,b)))