import random
def cost(theta,target):
	# the measurement of the guess will be written here
	# in our case the cost function consists of:
	# the rotation matrix, angle and the desired result
	return 0.0

# this hill climbing function is solving a minimization problem
def hillClimbing(search_space,target,error):
	theta=random.uniform(search_space[0],search_space[1])
	while cost(theta,target) < error:
		new_theta=random.uniform(search_space[0],search_space[1])
		if cost(theta,target) > cost(new_theta,target):
			theta=new_theta

	return theta


if __name__ == "__main__":
	tt=int(input())
	for i in range(tt):
		search_space=tuple(map(float,input().split()))
		target=float(input())
		error=float(input())
		print("Case #{}: {}".format(i+1,hillClimbing(search_space,target,0.1)))

	pass
