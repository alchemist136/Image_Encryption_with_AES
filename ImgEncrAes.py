# Code encrypts an RGB image into another cipher image
# keeping the dimensions and number of pixels almost same
# using AES

import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import numpy as np
from PIL import Image

# class implementing AES
class AESCipher(object):
    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plain_text):
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text)
        return (iv + encrypted_text)

    def decrypt(self, encrypted_text):
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:])
        return plain_text


# class implementing image encryption
class ImageEncryption:
    def __init__ (self, key):
        self.key = key
        self.aes = AESCipher(key)

    def __pad(self, arr):
        number_of_bytes_to_pad = self.aes.block_size - len(arr) % self.aes.block_size
        for _ in range(number_of_bytes_to_pad):
            arr.append(number_of_bytes_to_pad)
        return arr
    
    def __unpad(self, arr):
        to_remove = arr[len(arr)-1]
        return arr[:-to_remove]
    
    # encrypts each of the three rgb layers
    def __encrypt_layer_util(self, layer):
        (x,y) = layer.shape
        pixels = layer.flatten()
        pixels_util = []
        for p in pixels:
            pixels_util.append(p)
        pixels_util = self.__pad(pixels_util)
        byte_stream = bytearray(pixels_util)
        encr_stream = self.aes.encrypt(byte_stream)
        encr_pixels = []
        for b in encr_stream:
            encr_pixels.append(b)

        no_of_pixel_pad = y - len(encr_pixels)%y
        (new_x, new_y) = (int((len(encr_pixels)+no_of_pixel_pad)/y), y)

        for _ in range(no_of_pixel_pad):
            encr_pixels.append(new_x-x)
        layer_out = np.array(encr_pixels).reshape(new_x,new_y)
        return layer_out
    
    # decrypts each of the three rgb layers
    def __decrypt_layer_util(self, layer):
        pixels = layer.flatten()
        (x,y) = layer.shape
        added_row = pixels[-1]
        (new_x, new_y) = (x-added_row,y)
        aes_padding = self.aes.block_size - (new_x*new_y)%self.aes.block_size
        no_of_pixel_pad = len(pixels) - aes_padding - self.aes.block_size - new_x*new_y
        pixels = pixels[:-no_of_pixel_pad]
        pixels_util = []
        for p in pixels:
            pixels_util.append(p)
        byte_stream = bytearray(pixels_util)
        decr_stream = self.aes.decrypt(byte_stream)        
        decr_pixels = []
        for b in decr_stream:
            decr_pixels.append(b)
        decr_pixels = self.__unpad(decr_pixels)
        layer_out = np.array(decr_pixels).reshape(new_x,new_y)
        return layer_out
    
    def __encrypt_util(self, img_arr):
        (x,y,z) = img_arr.shape
        img_out = []
        for k in range(z):
            layer_out = self.__encrypt_layer_util(img_arr[:,:,k])
            img_out.append(layer_out)
        (p,q) = img_out[0].shape
        img_out = np.array(img_out)
        temp = [[[0 for _ in range(z)] for _ in range(q)] for _ in range(p)]
        for k in range(z):
            for i in range(p):
                for j in range(q):
                    temp[i][j][k] = img_out[k][i][j]
        return np.array(temp)
    
    def __decrypt_util(self, img_arr):
        (x,y,z) = img_arr.shape
        img_out = []
        for k in range(z):
            layer_out = self.__decrypt_layer_util(img_arr[:,:,k])
            img_out.append(layer_out)
        (p,q) = img_out[0].shape
        img_out = np.array(img_out)
        temp = [[[0 for _ in range(z)] for _ in range(q)] for _ in range(p)]
        for k in range(z):
            for i in range(p):
                for j in range(q):
                    temp[i][j][k] = img_out[k][i][j]
        return np.array(temp)

    def encrypt(self, in_file, out_file):
        try:
            img_in = np.asarray(Image.open(in_file))
            temp = self.__encrypt_util(img_in)
            temp = temp.astype('uint8')
            img_out = Image.fromarray(temp)
            img_out.save(out_file)
        except:
           raise Exception("Error in encryption")

    def decrypt(self, in_file, out_file):
        try:
            img_in = np.asarray(Image.open(in_file))
            temp = self.__decrypt_util(img_in)
            temp = temp.astype('uint8')
            img_out = Image.fromarray(temp)
            img_out.save(out_file)
        except:
            raise Exception("Error in decryption")
        


