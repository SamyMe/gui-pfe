# coding: utf-8

from sys import argv
from os import listdir
from os.path import isfile, join, isdir
from operator import itemgetter

import cPickle as pickle
import difflib

import scipy.spatial.distance

import matplotlib.pyplot as plt
import numpy as np

import lasagne
from lasagne.layers import InputLayer, DenseLayer, DropoutLayer
# from lasagne.layers.dnn import Conv2DDNNLayer as ConvLayer
from lasagne.layers import Conv2DLayer as ConvLayer
from lasagne.layers import MaxPool2DLayer as PoolLayer
from lasagne.layers import LocalResponseNormalization2DLayer as NormLayer
from lasagne.utils import floatX

#blocks imports
from theano import tensor, function
#theano imports
from theano_imports import dA

import io

import skimage


def prep_image(path):
    ext = path.split('.')[-1]

    # im = plt.imread(io.BytesIO(urllib.urlopen(url).read()), ext)
    im = plt.imread(path, ext)

    # Resize so smallest dim = 256, preserving aspect ratio
    h, w, _ = im.shape
    if h < w:
        im = skimage.transform.resize(im, (256, w*256/h), preserve_range=True)
    else:
        im = skimage.transform.resize(im, (h*256/w, 256), preserve_range=True)

    # Central crop to 224x224
    h, w, _ = im.shape
    im = im[h//2-112:h//2+112, w//2-112:w//2+112]

    rawim = np.copy(im).astype('uint8')

    # Shuffle axes to c01
    im = np.swapaxes(np.swapaxes(im, 1, 2), 0, 1)

    # Convert to BGR
    im = im[::-1, :, :]

    im = im - MEAN_IMAGE
    return rawim, floatX(im[np.newaxis])


def describe(path):
    rawim, im = prep_image(path)

    #4000a
    # result = np.array(lasagne.layers.get_output(net['fc6'], im, deterministic=True).eval())
    #4000b
    result = np.array(lasagne.layers.get_output(net['fc7'], im, deterministic=True).eval())
    #1000
    # result = np.array(lasagne.layers.get_output(net['fc8'], im, deterministic=True).eval())

    return result[0]




def createModels(myDir):

    modelsDB = {}
    for f in sorted(listdir(myDir)):
        if isfile(join(myDir, f)):
            print f
            desc = describe(myDir+f)
            modelsDB[myDir+f] = myFunction([desc,])[0]

    pickle.dump( modelsDB, open(myDir.split("/")[0]+"-model.pkl", "wb") )


def loadModel(path):
    model = pickle.load( open(path, "rb") )
    return model


def searchImage(image,model):

    topSim = []

    desc = describe(image)
    desc = myFunction([desc,])[0]

    for key in model.keys():

        sim = scipy.spatial.distance.euclidean(desc,model[key])
        if len(topSim)==5 and topSim[-1][1]>sim:
            topSim.pop()
            topSim.append((key,sim))
        elif len(topSim)<5:
            topSim.append((key,sim))
        topSim = sorted(topSim,key=itemgetter(1))


    return topSim
    #topSim contains dossier/image to extract directly


net = {}
net['input'] = InputLayer((None, 3, 224, 224))
net['conv1'] = ConvLayer(net['input'], num_filters=96, filter_size=7, stride=2, flip_filters=False)
net['norm1'] = NormLayer(net['conv1'], alpha=0.0001) # caffe has alpha = alpha * pool_size
net['pool1'] = PoolLayer(net['norm1'], pool_size=3, stride=3, ignore_border=False)
net['conv2'] = ConvLayer(net['pool1'], num_filters=256, filter_size=5, flip_filters=False)
net['pool2'] = PoolLayer(net['conv2'], pool_size=2, stride=2, ignore_border=False)
net['conv3'] = ConvLayer(net['pool2'], num_filters=512, filter_size=3, pad=1, flip_filters=False)
net['conv4'] = ConvLayer(net['conv3'], num_filters=512, filter_size=3, pad=1, flip_filters=False)
net['conv5'] = ConvLayer(net['conv4'], num_filters=512, filter_size=3, pad=1, flip_filters=False)
net['pool5'] = PoolLayer(net['conv5'], pool_size=3, stride=3, ignore_border=False)
net['fc6'] = DenseLayer(net['pool5'], num_units=4096)
net['drop6'] = DropoutLayer(net['fc6'], p=0.5)
net['fc7'] = DenseLayer(net['drop6'], num_units=4096)
net['drop7'] = DropoutLayer(net['fc7'], p=0.5)
net['fc8'] = DenseLayer(net['drop7'], num_units=1000, nonlinearity=lasagne.nonlinearities.softmax)
output_layer = net['fc8']



model_vgg = pickle.load(open('vgg_cnn_s.pkl'))


CLASSES = model_vgg['synset words']
MEAN_IMAGE = model_vgg['mean image']

lasagne.layers.set_all_param_values(output_layer, model_vgg['values'])

x = tensor.matrix('features')
# model_ae = pickle.load( open("AE-models/AE-Theano414.pkl") )
model_ae = pickle.load( open("AE-models/modelAE2-theano2.pkl") )

output = model_ae.get_hidden_values(x)
myFunction = function([x], output)


# createModels(argv[1])
model = loadModel("binocular-model.pkl")
# print len(model)
# image = argv[3]
# print searchImage(image,model)
