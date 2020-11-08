import Crypto.Random.random

amount = 2097152
InO = Crypto.Random.random.getrandbits(amount);
#print(SO)

FileHandler = open("/home/ftl/KuLab1/pyrandbits", "w" )

FileHandler.write("Here is PRBS of " +  str(amount) + " bits, written in integer in base 10\n")
FileHandler.write("------------------------------------------------------------------------\n")
FileHandler.write(str(InO))

FileHandler.close()

