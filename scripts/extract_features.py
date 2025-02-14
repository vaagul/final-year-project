import sys
import os.path
import argparse

import numpy as np
from scipy.misc import imread, imresize
import scipy.io

parser = argparse.ArgumentParser()
parser.add_argument('--caffe', help='path to caffe installation')
parser.add_argument('--model_def', help='path to model definition prototxt')
parser.add_argument('--model', help='path to model parameters')
parser.add_argument('--gpu', action='store_true', help='whether to use gpu')
parser.add_argument('--image', help='path to image')

args = parser.parse_args()

if args.caffe:
    caffepath = args.caffe + '/python'
    sys.path.append(caffepath)

import caffe

def predict(in_data, net):

    out = net.forward(**{net.inputs[0]: in_data})
    features = out[net.outputs[0]]
    return features


def batch_predict(filenames, net):

    N, C, H, W = net.blobs[net.inputs[0]].data.shape
    F = net.blobs[net.outputs[0]].data.shape[1]
    Nf = len(filenames)
    Hi, Wi, _ = imread(filenames[0]).shape
    allftrs = np.zeros((Nf, F))
    for i in range(0, Nf, N):
        in_data = np.zeros((N, C, H, W), dtype=np.float32)

        batch_range = range(i, min(i+N, Nf))
        batch_filenames = [filenames[j] for j in batch_range]
        Nb = len(batch_range)

        batch_images = np.zeros((Nb, 3, H, W))
        for j,fname in enumerate(batch_filenames):
            im = imread(fname)
            if len(im.shape) == 2:
                im = np.tile(im[:,:,np.newaxis], (1,1,3))
            im = im[:,:,(2,1,0)]
            im = im - np.array([103.939, 116.779, 123.68])
            im = imresize(im, (H, W), 'bicubic')
            im = np.transpose(im, (2, 0, 1))
            batch_images[j,:,:,:] = im

        in_data[0:len(batch_range), :, :, :] = batch_images

        ftrs = predict(in_data, net)

        for j in range(len(batch_range)):
            allftrs[i+j,:] = ftrs[j,:]

        print 'Done %d/%d files' % (i+len(batch_range), len(filenames))

    return allftrs


if args.gpu:
    caffe.set_mode_gpu()
else:
    caffe.set_mode_cpu()

net = caffe.Net(args.model_def, args.model, caffe.TEST)

base_dir = os.path.dirname(args.image)

allftrs = batch_predict([args.image], net)

scipy.io.savemat(os.path.join(base_dir, 'vgg_feats.mat'), mdict =  {'feats': np.transpose(allftrs)})
