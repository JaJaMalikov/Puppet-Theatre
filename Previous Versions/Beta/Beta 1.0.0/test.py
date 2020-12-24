import data
import copy
import random

thingus = {"one":copy.deepcopy(data.default), 
			"two":copy.deepcopy(data.default), 
			"three":copy.deepcopy(data.default)}

thingus["one"]["pos"][2] = random.randrange(0,10)
thingus["two"]["pos"][2] = random.randrange(0,10)
thingus["three"]["pos"][2] = random.randrange(0,10)

default_order = list(range(0,len(thingus)))


for y in sorted(thingus, key = lambda x: thingus[x]["pos"][2]):
	print(y)
