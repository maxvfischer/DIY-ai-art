from StyleGAN import StyleGAN
import argparse
from utils import *

"""parsing and configuration"""
def parse_args():
    desc = "Tensorflow implementation of StyleGAN"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--batch_size', type=int, default=1, help='The size of batch in the test phase')
    parser.add_argument('--sn', type=str2bool, default=False, help='use spectral normalization')
    parser.add_argument('--img_size', type=int, default=1024, help='The target size of image')
    parser.add_argument('--test_num', type=int, default=100, help='The number of generating images in the test phase')

    parser.add_argument('--checkpoint_dir', type=str, default='checkpoint',
                        help='Directory name to save the checkpoints')
    parser.add_argument('--result_dir', type=str, default='results',
                        help='Directory name to save the generated images')
    
    return parser.parse_args()



"""main"""
def main():
    # parse arguments
    args = parse_args()
    if args is None:
      exit()

    # open session
    config = tf.ConfigProto(allow_soft_placement=True)
    #config.gpu_options.per_process_gpu_memory_fraction = 0.8
    with tf.Session(config=config) as sess:

        gan = StyleGAN(
            sess=sess,
            batch_size=args.batch_size,
            img_size=args.img_size,
            test_num=args.test_num,
            checkpoint_dir=args.checkpoint_dir,
            result_dir=args.result_dir)

        # build graph
        gan.build_model()

        gan.generate()


if __name__ == '__main__':
    main()
