import string

import tensorflow as tf

import captcha_model
import generate_captcha

def test_captcha():
    captcha = generate_captcha.generateCaptcha(width=100, height=30, characters=string.digits)
    width, height, char_num, characters, classes = captcha.get_parameter()

    x = tf.placeholder(tf.float32, [None, height, width, 1])
    y_ = tf.placeholder(tf.float32, [None, char_num * classes])
    keep_prob = tf.placeholder(tf.float32)

    model = captcha_model.captchaModel(width, height, char_num, classes)
    y_conv = model.create_model(x, keep_prob)
    cross_entropy = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y_, logits=y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    predict = tf.reshape(y_conv, [-1, char_num, classes])
    real = tf.reshape(y_, [-1, char_num, classes])
    correct_prediction = tf.equal(tf.argmax(predict, 2), tf.argmax(real, 2))
    correct_prediction = tf.cast(correct_prediction, tf.float32)
    accuracy = tf.reduce_mean(correct_prediction)

    saver = tf.train.Saver()
    with tf.Session() as sess:
        # sess.run(tf.global_variables_initializer())
        saver.restore(sess, tf.train.latest_checkpoint("./ckpt"))
        # batch_x, batch_y = captcha.gen_test_captcha()
        batch_x, batch_y = captcha.gen_api_captcha()
        loss = sess.run([y_conv], feed_dict={x: batch_x, y_: batch_y, keep_prob: 0.75})

    print("real == %s, predict = %s, result = %s" % (captcha.decode_captcha(batch_y), captcha.decode_captcha(loss),
                                                     "Match" if captcha.decode_captcha(
                                                         batch_y) == captcha.decode_captcha(loss) else "Not Match"))
    return True if captcha.decode_captcha(batch_y) == captcha.decode_captcha(loss) else False


if __name__ == '__main__':
    test_captcha()
