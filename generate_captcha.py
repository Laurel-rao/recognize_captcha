# -*- coding:utf-8 -*-
import base64
import json
import os
import uuid

import requests
from captcha.image import ImageCaptcha
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import random
import string


class generateCaptcha():
    def __init__(self,
                 width=100,  # 验证码图片的宽
                 height=30,  # 验证码图片的高
                 char_num=4,  # 验证码字符个数
                 characters=string.digits + string.ascii_uppercase + string.ascii_lowercase):  # 验证码组成，数字+大写字母+小写字母
        self.width = width
        self.height = height
        self.char_num = char_num
        self.characters = characters
        self.classes = len(characters)


    def download(self):
        resp = requests.get("https://app.huawei.com/escpportal/servlet/identifying", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"})
        name = uuid.uuid4().hex
        with open("./test_image/%s.jpg" % name, "wb") as ff:
            data = resp.content
            ff.write(resp.content)
        return name, data

    def get_result(self, img_data):
        result = self.base64_api(uname='xxx', pwd='xxx', img_data=img_data)
        return result

    def base64_api(self, uname, pwd, img_data):
        base64_data = base64.b64encode(img_data)
        b64 = base64_data.decode()
        data = {"username": uname, "password": pwd, "image": b64, "typeid": 1}
        result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            return result["message"]

    def gen_captcha(self, batch_size=50):
        X = np.zeros([batch_size, self.height, self.width, 1])
        img = np.zeros((self.height, self.width), dtype=np.uint8)
        Y = np.zeros([batch_size, self.char_num, self.classes])
        # image = ImageCaptcha(width=self.width, height=self.height)

        while True:
            for i in range(batch_size):
                # img = image.generate_image(captcha_str).convert('L')
                filename = random.choice(self.files)

                image = Image.open(os.path.join("./total_image/", filename)).convert("L")
                img = np.array(image)
                captcha_str = self.data.get(filename.replace(".jpg", ""))
                if captcha_str is None:
                    print(os.path.join("./total_image/", filename))
                # if captcha_str is None:
                #     os.remove(os.path.join("./huawei_image/", filename))
                #     filename = random.choice(self.files)
                #     image = Image.open(os.path.join("./huawei_image/", filename)).convert("L")
                #     # plt.imshow(img)
                #     # plt.axis('off')
                #     # plt.show()
                #     img = np.array(image)
                #     captcha_str = self.data.get(filename.replace(".jpg", ""))
                X[i] = np.reshape(img, [self.height, self.width, 1]) / 255.0
                for j, ch in enumerate(captcha_str):
                    Y[i, j, self.characters.find(ch)] = 1
            Y = np.reshape(Y, (batch_size, self.char_num * self.classes))
            yield X, Y

    def from_local_file_captcha(self):

        img = Image.open("./image/identifying.jpg")
        img = img.resize((160, 60))
        img.show()
        X = np.zeros([1, self.height, self.width, 1])
        Y = np.zeros([1, self.char_num, self.classes])
        img = img.convert('L')
        img = np.array(img.getdata())
        X[0] = np.reshape(img, [self.height, self.width, 1]) / 255.0
        captcha_str = "2888"
        for j, ch in enumerate(captcha_str):
            Y[0, j, self.characters.find(ch)] = 1
        Y = np.reshape(Y, (1, self.char_num * self.classes))
        return X, Y

    def decode_captcha(self, y):
        y = np.reshape(y, (len(y), self.char_num, self.classes))
        return ''.join(self.characters[x] for x in np.argmax(y, axis=2)[0, :])

    def get_parameter(self):
        return self.width, self.height, self.char_num, self.characters, self.classes

    def gen_test_captcha(self):

        filename = random.choice(self.files)

        captcha_str = self.data.get(filename.replace(".jpg", ""))
        if captcha_str is None:
            print(os.path.join("./total_image/", filename))
        img = Image.open(os.path.join("./total_image/", filename))

        X = np.zeros([1, self.height, self.width, 1])
        Y = np.zeros([1, self.char_num, self.classes])
        img = img.convert('L')
        img = np.array(img.getdata())
        X[0] = np.reshape(img, [self.height, self.width, 1]) / 255.0
        # captcha_str = "1231"
        for j, ch in enumerate(captcha_str):
            Y[0, j, self.characters.find(ch)] = 1
        Y = np.reshape(Y, (1, self.char_num * self.classes))
        return X, Y

    def gen_api_captcha(self):
        name, data = self.download()
        img = Image.open(os.path.join("./test_image/%s.jpg" % name))
        captcha_str = self.get_result(data)
        print("name == %s, str = %s" % (name, captcha_str))
        X = np.zeros([1, self.height, self.width, 1])
        Y = np.zeros([1, self.char_num, self.classes])
        img = img.convert('L')
        img = np.array(img.getdata())
        X[0] = np.reshape(img, [self.height, self.width, 1]) / 255.0
        # captcha_str = "1231"
        for j, ch in enumerate(captcha_str):
            Y[0, j, self.characters.find(ch)] = 1
        Y = np.reshape(Y, (1, self.char_num * self.classes))
        return X, Y

    def gen_local_captcha(self, file_path):
        img = Image.open(file_path)
        X = np.zeros([1, self.height, self.width, 1])
        Y = np.zeros([1, self.char_num, self.classes])
        img = img.convert('L')
        img = np.array(img.getdata())
        X[0] = np.reshape(img, [self.height, self.width, 1]) / 255.0
        captcha_str = "1231"
        for j, ch in enumerate(captcha_str):
            Y[0, j, self.characters.find(ch)] = 1
        Y = np.reshape(Y, (1, self.char_num * self.classes))
        return X, Y