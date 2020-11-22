from Crypto import Random
from Crypto.Random import random
from Crypto.PublicKey import ElGamal
from Crypto.Util.number import GCD
from Crypto.Hash import HMAC
from Crypto.Hash import MD5
from Crypto.Hash import SHA512


import json
import os

hashes = {'HMAC':HMAC, 'MD5':MD5, 'SHA512':SHA512}

class Key:
    def __init__(self, key):
        self.key = key

    @classmethod
    def generate_key(cls, bitlength):
        key = ElGamal.generate(bitlength, Random.new().read)
        return cls(key)

    def save_key(self, file_to_save):
        key_dict = {'p': self.key.p, 'g': self.key.g, 
        'y': self.key.y, 'x': self.key.x}

        with open(file_to_save, 'w+') as file:
            json.dump(key_dict, file)

    @classmethod
    def read_key(cls, file_to_read):
        with open(file_to_read, 'r') as file:
            key_dict = json.load(file)

        key = ElGamal.construct((key_dict['p'], key_dict['g'], key_dict['y'], key_dict['x']))
        return cls(key)

    def save_pub(self, file_to_save):
        pub_key_dict = {'p': self.key.p, 'g': self.key.g, 'y': self.key.y}

        with open(file_to_save, 'w+') as file:
            json.dump(pub_key_dict, file)

    @classmethod
    def read_pub(cls, file_to_read):
        with open(file_to_read, 'r') as file:
            pub_key_dict = json.load(file)

        key = ElGamal.construct((pub_key_dict['p'], pub_key_dict['g'], pub_key_dict['y'], -1))
        return cls(key.publickey())


def sign(message, key, hash_alg):
    h = hashes[hash_alg].new(message.encode()).digest()

    while True:
        k = random.StrongRandom().randint(1, key.key.p-1)
        if GCD(k, key.key.p-1) == 1: 
            break

    sign = key.key.sign(h,k)
    return {'message': message, 'signature': sign, 'hash_alg':hash_alg}


def save_sign(sign_dict, file_to_save):
    with open(file_to_save, 'w+') as file:
        json.dump(sign_dict, file)

def read_sign(file_to_save):
    with open(file_to_save, 'r') as file:
        return json.load(file)

def verify(message, sign, pub_key, hash_alg):
    h = hashes[hash_alg].new(message.encode()).digest()
    return pub_key.key.verify(h, sign)

def SIGN_AND_VERIFY(keylength, message, index, hash_alg):
    
    print("test case: " + index + "; key length = " + str(keylength) + "; message = " + message + "; hash alg = " + hash_alg)
    keyA = Key.generate_key(keylength)
    keyA.save_pub(os.path.join(key_folder, 'pub' + index +'.json'))
    sign_dict = sign(message, keyA, hash_alg)    

    save_sign(sign_dict, os.path.join(sign_folder, 'sign' + index +'.json'))

    pubA = Key.read_pub(os.path.join(key_folder, 'pub' + index +'.json'))
    read_sign_dict = read_sign(os.path.join(sign_folder, 'sign' + index +'.json'))
    messageA, signA, hash_alg = read_sign_dict['message'], read_sign_dict['signature'], read_sign_dict['hash_alg']

    print(verify(messageA, signA, pubA, hash_alg))
    

if __name__ == '__main__':
    sign_folder = "signatures"
    os.makedirs(sign_folder, exist_ok=True)
    key_folder = "keys"
    os.makedirs(key_folder, exist_ok=True)
    
    #SIGN_AND_VERIFY(32, 'I have one million dollars!', '0', 'HMAC')
    #SIGN_AND_VERIFY(64, 'I do not have one million dollars!', '1', 'MD5')
    #SIGN_AND_VERIFY(128, 'Maybe I have one million dollars!', '2', 'SHA512')
    #SIGN_AND_VERIFY(256, 'I am definetly sure that I have one million dollars!', '3', 'HMAC')
    #SIGN_AND_VERIFY(512, 'Know what, maybe I had one million dollars', '4', 'MD5')
    #SIGN_AND_VERIFY(1024, 'I am Alice', '5', 'SHA512')
    #SIGN_AND_VERIFY(2048, 'And I am Bob', '6', 'HMAC')
    #SIGN_AND_VERIFY(32, 'I like pudding! Truly true!', '7', 'MD5')
    #SIGN_AND_VERIFY(64, 'I am prepared for exam', '8', 'SHA512')
    #SIGN_AND_VERIFY(128, 'No, I was not drinking with my friends yesterday, honey', '9', 'HMAC')

    pubA = Key.read_pub(os.path.join(key_folder, 'pub9.json'))
    read_sign_dict = read_sign(os.path.join(sign_folder, 'sign9.json'))
    messageA, signA, hash_alg = read_sign_dict['message'], read_sign_dict['signature'], read_sign_dict['hash_alg']

    print(verify(messageA, signA, pubA, hash_alg))
    
    read_sign_dict = read_sign(os.path.join(sign_folder, 'sign2.json'))
    messageA, signA, hash_alg = read_sign_dict['message'], read_sign_dict['signature'], read_sign_dict['hash_alg']

    print(verify(messageA, signA, pubA, hash_alg))

    read_sign_dict = read_sign(os.path.join(sign_folder, 'sign3.json'))
    messageA, signA, hash_alg = read_sign_dict['message'], read_sign_dict['signature'], read_sign_dict['hash_alg']

    print(verify(messageA, signA, pubA, hash_alg))

    read_sign_dict = read_sign(os.path.join(sign_folder, 'sign4.json'))
    messageA, signA, hash_alg = read_sign_dict['message'], read_sign_dict['signature'], read_sign_dict['hash_alg']
    
    print(verify(messageA, signA, pubA, hash_alg))

    read_sign_dict = read_sign(os.path.join(sign_folder, 'sign9_CORRUPT_HASH.json'))
    messageA, signA, hash_alg = read_sign_dict['message'], read_sign_dict['signature'], read_sign_dict['hash_alg']

    #print(verify(messageA, signA, pubA, hash_alg))
    
    read_sign_dict = read_sign(os.path.join(sign_folder, 'sign9_CORRUPT_KEY.json'))
    messageA, signA, hash_alg = read_sign_dict['message'], read_sign_dict['signature'], read_sign_dict['hash_alg']

    #print(verify(messageA, signA, pubA, hash_alg))
    
    read_sign_dict = read_sign(os.path.join(sign_folder, 'sign9_CORRUPT_TEXT.json'))
    messageA, signA, hash_alg = read_sign_dict['message'], read_sign_dict['signature'], read_sign_dict['hash_alg']

   # print(verify(messageA, signA, pubA, hash_alg))
