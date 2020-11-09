import Crypto.Random.random

#amount = 2097152

FileHandler = open("/home/ftl/KuLab1/pyrandbits", "w" )
samount = 64
for i in range(32768):
    InO = Crypto.Random.random.getrandbits(samount);
    i= i + 1
    FileHandler.write(str(InO))
    FileHandler.write('\n')

FileHandler.close()

