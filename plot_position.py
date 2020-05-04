import db_metre
import math

# the wifi class
class wifi:
	position=(0.0,0.0)
	signalDB=0.0
	freq=0.0

# the rotation function 
def rotateVector(theta,vector):
	return (vector[0]*math.cos(theta)-vector[1]*math.sin(theta),vector[1]*math.sin(theta)+vector[1]*math.cos(theta))

def cost(theta,target,device,closest_wifi,next_wifi):
	# the measurement of the guess will be written here
	# in our case the cost function consists of:
	# the rotation matrix, angle and the desired result
	# it return the absolute difference between the already rotated device and...
	# ...the next wifi
	device=(device[0]-closest_wifi[0],device[1]-closest_wifi[1])
	device=rotateVector(theta,device)
	device=(device[0]+closest_wifi[0],device+device[1]+closest_wifi[1])
	dist=math.sqrt((next_wifi[0]-device[0])**2 -(next_wifi[1]-device[1])**2)
	return math.abs(dist-target)


# this hill climbing function is solving a minimization problem
def hillClimbing(search_space,target,device,closest_wifi,next_wifi):
	theta=random.uniform(search_space[0],search_space[1])
	best=cost(theta,target,closest_wifi,device,next_wifi)
	
	while cost(theta,target,closest_wifi,device,next_wifi) < .001:
		new_theta=random.uniform(search_space[0],search_space[1])
		if best > cost(new_theta,target,closest_wifi,device,next_wifi):
			new_theta=theta
			best=cost(new_theta,target,closest_wifi,device,next_wifi)
	
	return theta

# min function to find the index of the shortest distance
def miniDistIndex(distances):
	min_index=0
	for i in range(1,len(distances)):
		if distances[i] < distances[min_index]:
			min_index=i
	return min_index

# this function finds the position of a device 
def devPos(wifiobj):
	# for each wifi router or hotspot
	# find the distance between the routers and the device
	# find the minimum distance between the devices
	distances=[]
	for x in wifiobj:
		distances.append(db_metre.dist(x.signal,x.freq))
	
	min_index=minDistIndex(distances)

	closest_wifi=wifiobj[min_index].position
	init_pos=(closest_wifi[0],closest_wifi[1]+distances[min_index])
	
	# make the closest wifi the origin of the device
	# then find the angle between the next closest wifi 
	distances.pop(min_index)
	min_index=minDistIndex(distances)
	next_wifi=(wifiobj[min_index].position[0],wifiobj[min_index].position[1])

	# find the angle theta between the device and the next wifi 
	theta=hillClimbing((0,2*math.pi),distances[min_index],init_pos,closest_wifi,next_wifi)
	
	# rotate the device by an angle theta
	result=(init_pos[0]-closest_wifi[0],init_pos[1]-closest_wifi[1])
	result=rotateVector(theta,result)
	result=(result[0]+closest_wifi[0],result[1]+closest_wifi[1])
	
	return result


if __name__ == "__main__":
	tt=int(input())
	for i in range(tt):
		kk=int(input())
		wifi_list=[]
		for j in range(kk):
			temp=list(map(float,input().split()))
			temp_wifi=wifi()
			temp_wifi.signalDB=temp[0]
			temp_wifi.freq=temp[1]
			temp_wifi.position[0]=temp[2]
			temp_wifi.position[1]=temp[3]
			wifi_list.append(temp_wifi)

		print("Case #{}:{}".format(i+1,devPos(wifi_list)))