from ImgEncrAes import ImageEncryption
from tqdm import tqdm


key = "This is a key for demonstration"
imgEn = ImageEncryption(key)

no_of_img = 2
for j in tqdm (range(no_of_img), desc="Encrypting..."):
    imgEn.encrypt("plain_img_1.jpg","cipher_img_1.png")
    imgEn.encrypt("plain_img_2.jpg","cipher_img_2.png")

print("Encryption Complete !!")

for j in tqdm (range(no_of_img), desc="Decrypting..."):
    imgEn.decrypt("cipher_img_1.png","decrypted_plain_img_1.jpg")
    imgEn.decrypt("cipher_img_2.png","decrypted_plain_img_2.jpg")

print("Decryption Complete !!")
