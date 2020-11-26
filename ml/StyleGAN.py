import time
from ml.ops import *
from ml.utils import *
import tensorflow as tf
from tensorflow.contrib.data import prefetch_to_device, shuffle_and_repeat, map_and_batch
import numpy as np
import PIL.Image
from tqdm import tqdm
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import multiprocessing

class StyleGAN(object):
    """
    
    """
    def __init__(self, 
                 sess: tf.Session,
                 batch_size: int,
                 img_size: int,
                 checkpoint_directory: str,
                 image_directory: str,
                 sn: bool = False) -> None:
        check_folder(image_directory)

        self.sess = sess
        self.checkpoint_directory = checkpoint_directory
        self.image_directory = image_directory
        self.batch_size = batch_size
        self.img_size = img_size
        self.z_dim = 512
        self.w_dim = 512
        self.n_mapping = 8
        self.truncation_psi = 0.7 # Style strength multiplier for the truncation trick
        self.truncation_cutoff = 8 # Number of layers for which to apply the truncation trick
        self.sn = sn

        # Build GAN model
        self.build_model()
        tf.global_variables_initializer().run()
        self.saver = tf.train.Saver()
        self.load_checkpoint(self.checkpoint_directory)


    def generate_images(self,
                        num_images: int):
        image_frame_dim = int(np.floor(np.sqrt(self.batch_size)))

        for i in tqdm(range(num_images)):
            if self.batch_size == 1:
                seed = np.random.randint(low=0, high=1000000)
                test_z = tf.cast(np.random.RandomState(seed).normal(size=[self.batch_size, self.z_dim]), tf.float32)
                alpha = tf.constant(0.0, dtype=tf.float32, shape=[])
                self.fake_images = self.generator(test_z, alpha=alpha, target_img_size=self.img_size, is_training=False)
                samples = self.sess.run(self.fake_images)

                save_images(samples[:image_frame_dim * image_frame_dim, :, :, :], [image_frame_dim, image_frame_dim],
                            '{}/artwork_{}.jpg'.format(self.image_directory, int(time.time())))
            else:
                samples = self.sess.run(self.fake_images)

                save_images(samples[:image_frame_dim * image_frame_dim, :, :, :], [image_frame_dim, image_frame_dim],
                            '{}/artwork_{}.jpg'.format(self.image_directory, int(time.time())))

    def load_checkpoint(self, checkpoint_dir):
        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
        ckpt_name = "StyleGAN.model-1662968"
        self.saver.restore(self.sess, os.path.join(checkpoint_dir, ckpt_name))

    def generator(self, z, alpha, target_img_size, is_training=True, reuse=tf.AUTO_REUSE):
        with tf.variable_scope("generator", reuse=reuse):
            resolutions = resolution_list(target_img_size)
            featuremaps = featuremap_list(target_img_size)

            w_avg = tf.get_variable('w_avg', shape=[self.w_dim],
                                    dtype=tf.float32, initializer=tf.initializers.zeros(),
                                    trainable=False, aggregation=tf.VariableAggregation.ONLY_FIRST_TOWER)

            """ mapping layers """
            n_broadcast = len(resolutions) * 2
            w_broadcasted = self.g_mapping(z, n_broadcast)

            """ apply truncation trick on evaluation """
            w_broadcasted = self.truncation_trick(n_broadcast, w_broadcasted, w_avg, self.truncation_psi)

            """ synthesis layers """
            x = self.g_synthesis(w_broadcasted, alpha, resolutions, featuremaps)

            return x

    def g_mapping(self, z, n_broadcast, reuse=tf.AUTO_REUSE):
        with tf.variable_scope('g_mapping', reuse=reuse):
            # normalize input first
            x = pixel_norm(z)

            # run through mapping network
            for ii in range(self.n_mapping):
                with tf.variable_scope('FC_{:d}'.format(ii)):
                    x = fully_connected(x, units=self.w_dim, gain=np.sqrt(2), lrmul=0.01)
                    x = apply_bias(x, lrmul=0.01)
                    x = lrelu(x, alpha=0.2)

            # broadcast to n_layers
            with tf.variable_scope('Broadcast'):
                x = tf.tile(x[:, np.newaxis], [1, n_broadcast, 1])

        return x

    def truncation_trick(self, n_broadcast, w_broadcasted, w_avg, truncation_psi):
        with tf.variable_scope('truncation'):
            layer_indices = np.arange(n_broadcast)[np.newaxis, :, np.newaxis]
            ones = np.ones(layer_indices.shape, dtype=np.float32)
            coefs = tf.where(layer_indices < self.truncation_cutoff, truncation_psi * ones, ones)
            w_broadcasted = lerp(w_avg, w_broadcasted, coefs)

        return w_broadcasted

    def g_synthesis(self, w_broadcasted, alpha, resolutions, featuremaps, reuse=tf.AUTO_REUSE):
        with tf.variable_scope('g_synthesis', reuse=reuse):
            coarse_styles, middle_styles, fine_styles = get_style_class(resolutions, featuremaps)
            layer_index = 2

            """ initial layer """
            res = resolutions[0]
            n_f = featuremaps[0]

            x = synthesis_const_block(res, w_broadcasted, n_f, self.sn)

            """ remaining layers """
            images_out = torgb(x, res=res, sn=self.sn)
            coarse_styles.pop(res, None)

            # Coarse style [4 ~ 8]
            # pose, hair, face shape
            for res, n_f in coarse_styles.items():
                x = synthesis_block(x, res, w_broadcasted, layer_index, n_f, sn=self.sn)
                img = torgb(x, res, sn=self.sn)
                images_out = upscale2d(images_out)
                images_out = smooth_transition(images_out, img, res, resolutions[-1], alpha)

                layer_index += 2

            # Middle style [16 ~ 32]
            # facial features, eye
            for res, n_f in middle_styles.items():
                x = synthesis_block(x, res, w_broadcasted, layer_index, n_f, sn=self.sn)
                img = torgb(x, res, sn=self.sn)
                images_out = upscale2d(images_out)
                images_out = smooth_transition(images_out, img, res, resolutions[-1], alpha)

                layer_index += 2

            # Fine style [64 ~ 1024]
            # color scheme
            for res, n_f in fine_styles.items():
                x = synthesis_block(x, res, w_broadcasted, layer_index, n_f, sn=self.sn)
                img = torgb(x, res, sn=self.sn)
                images_out = upscale2d(images_out)
                images_out = smooth_transition(images_out, img, res, resolutions[-1], alpha)

                layer_index += 2

            return images_out

    def build_model(self):
        test_z = tf.random_normal(shape=[self.batch_size, self.z_dim])
        alpha = tf.constant(0.0, dtype=tf.float32, shape=[])
        self.fake_images = self.generator(test_z, alpha=alpha, target_img_size=self.img_size, is_training=False)



class GANEventHandler(FileSystemEventHandler):
    def __init__(self,
                 batch_size: int,
                 img_size: int,
                 test_num: int,
                 checkpoint_directory: str,
                 image_directory: str,
                 lower_limit_num_images: int):
        self.batch_size = batch_size
        self.img_size = img_size
        self.test_num = test_num
        self.checkpoint_directory = checkpoint_directory
        self.image_directory = image_directory
        self.lower_limit_num_images = lower_limit_num_images
        self.generating_images = multiprocessing.Value('b', False)

    def generate_images(self,
                        generating_images):
        generating_images.value = True
        
        config = tf.ConfigProto(allow_soft_placement=True)
        with tf.Session(config=config) as sess:
            gan = StyleGAN(
                sess=sess,
                batch_size=self.batch_size,
                img_size=self.img_size,
                checkpoint_directory=self.checkpoint_directory,
                image_directory=self.image_directory)

            gan.generate_images(
                num_images=self.test_num
            )
        
        generating_images.value = False

    def on_deleted(self,
                   event):
        image_names = [image_name for image_name in os.listdir(self.image_directory) if '.jpg' in image_name]
        num_images = len(image_names)
        if (num_images < self.lower_limit_num_images) and (self.generating_images.value == False):
            p_generate = multiprocessing.Process(
                target=self.generate_images,
                args=(self.generating_images,)
            )
            p_generate.start()
