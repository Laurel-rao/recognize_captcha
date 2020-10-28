import string

import tensorflow as tf

import captcha_model
import generate_captcha


def test_captcha(file_path):
    captcha = generate_captcha.generateCaptcha(width=100, height=30, characters=string.digits)
    width, height, char_num, characters, classes = captcha.get_parameter()

    x = tf.placeholder(tf.float32, [None, height, width, 1])
    y_ = tf.placeholder(tf.float32, [None, char_num * classes])
    keep_prob = tf.placeholder(tf.float32)

    model = captcha_model.captchaModel(width, height, char_num, classes)
    y_conv = model.create_model(x, keep_prob)

    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, tf.train.latest_checkpoint("./ckpt"))
        batch_x, batch_y = captcha.gen_local_captcha(file_path)
        loss = sess.run([y_conv], feed_dict={x: batch_x, y_: batch_y, keep_prob: 0.75})
    return captcha.decode_captcha(loss)


print(test_captcha("./test_image/1ea24f94240a44569dc288290c004b4a.jpg"))
