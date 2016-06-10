# coding: utf-8

#THEANO AE imports
from theano import function
import theano
import theano.tensor as T
from theano.tensor.shared_randomstreams import RandomStreams
#end THEANO AE imports

#Theano LBP imports
from skimage import data
from skimage.color import rgb2gray
from skimage.feature import local_binary_pattern
from skimage.feature import greycomatrix, greycoprops
from os.path import abspath
import numpy as np
import scipy
#end Theano LBP imports



class dA(object):
    def __init__(
        self,
        numpy_rng,
        theano_rng=None,
        input=None,
        n_visible=784,
        n_hidden=500,
        W=None,
        bhid=None,
        bvis=None
    ):
        self.n_visible = n_visible
        self.n_hidden = n_hidden

        # create a Theano random generator that gives symbolic random values
        if not theano_rng:
            theano_rng = RandomStreams(numpy_rng.randint(2 ** 30))

        # note : W' was written as `W_prime` and b' as `b_prime`
        if not W:
            # W is initialized with `initial_W` which is uniformely sampled
            # from -4*sqrt(6./(n_visible+n_hidden)) and
            # 4*sqrt(6./(n_hidden+n_visible))the output of uniform if
            # converted using asarray to dtype
            # theano.config.floatX so that the code is runable on GPU
            initial_W = np.asarray(
                numpy_rng.uniform(
                    low=-4 * np.sqrt(6. / (n_hidden + n_visible)),
                    high=4 * np.sqrt(6. / (n_hidden + n_visible)),
                    size=(n_visible, n_hidden)
                ),
                dtype=theano.config.floatX
            )
            W = theano.shared(value=initial_W, name='W', borrow=True)

        if not bvis:
            bvis = theano.shared(
                value=np.zeros(
                    n_visible,
                    dtype=theano.config.floatX
                ),
                borrow=True
            )

        if not bhid:
            bhid = theano.shared(
                value=np.zeros(
                    n_hidden,
                    dtype=theano.config.floatX
                ),
                name='b',
                borrow=True
            )

        self.W = W
        # b corresponds to the bias of the hidden
        self.b = bhid
        # b_prime corresponds to the bias of the visible
        self.b_prime = bvis
        # tied weights, therefore W_prime is W transpose
        self.W_prime = self.W.T
        self.theano_rng = theano_rng
        # if no input is given, generate a variable representing the input
        if input is None:
            # we use a matrix because we expect a minibatch of several
            # examples, each example being a row
            self.x = T.dmatrix(name='input')
        else:
            self.x = input

        self.params = [self.W, self.b, self.b_prime]

    def get_corrupted_input(self, input, corruption_level):
        """This function keeps ``1-corruption_level`` entries of the inputs the
        same and zero-out randomly selected subset of size ``coruption_level``
        Note : first argument of theano.rng.binomial is the shape(size) of
               random numbers that it should produce
               second argument is the number of trials
               third argument is the probability of success of any trial

                this will produce an array of 0s and 1s where 1 has a
                probability of 1 - ``corruption_level`` and 0 with
                ``corruption_level``

                The binomial function return int64 data type by
                default.  int64 multiplicated by the input
                type(floatX) always return float64.  To keep all data
                in floatX when floatX is float32, we set the dtype of
                the binomial to floatX. As in our case the value of
                the binomial is always 0 or 1, this don't change the
                result. This is needed to allow the gpu to work
                correctly as it only support float32 for now.

        """
        return self.theano_rng.binomial(size=input.shape, n=1,
                                        p=1 - corruption_level,
                                        dtype=theano.config.floatX) * input

    def get_hidden_values(self, input):
        """ Computes the values of the hidden layer """
        return T.nnet.sigmoid(T.dot(input, self.W) + self.b)

    def get_reconstructed_input(self, hidden):
        """Computes the reconstructed input given the values of the
        hidden layer

        """
        return T.nnet.sigmoid(T.dot(hidden, self.W_prime) + self.b_prime)

    def get_cost_updates(self, corruption_level, learning_rate):
        """ This function computes the cost and the updates for one trainng
        step of the dA """

        tilde_x = self.get_corrupted_input(self.x, corruption_level)
        y = self.get_hidden_values(tilde_x)
        z = self.get_reconstructed_input(y)
        # note : we sum over the size of a datapoint; if we are using
        #        minibatches, L will be a vector, with one entry per
        #        example in minibatch
        L = T.sqrt(T.sum((self.x - z)**2, axis=1))

        # note : L is now a vector, where each element is the
        #        cross-entropy cost of the reconstruction of the
        #        corresponding example of the minibatch. We need to
        #        compute the average of all these to get the cost of
        #        the minibatch
        cost = T.mean(L)

        # compute the gradients of the cost of the `dA` with respect
        # to its parameters
        gparams = T.grad(cost, self.params)
        # generate the list of updates
        updates = [
            (param, param - learning_rate * gparam)
            for param, gparam in zip(self.params, gparams)
        ]

        return (cost, updates)


def generate(path):

    # ####### LBP ######## #
    img = data.load(abspath(path))
    img_gray = rgb2gray(img)
    img_gray *= 255

    img_lbp = local_binary_pattern(
                    img_gray, 8, 1, method='nri_uniform'
                    )

    histogram = np.hstack((img_lbp.flatten(), list(range(59))))
    histogram = scipy.stats.itemfreq(histogram)
    # print histogram.shape

    try:
        a, b, c = img.shape
    except:
        a, b = img.shape

    # We know they are equal:
    # print a*b
    # print sum(a[1] for a in histogram)

    # lbp histogram values Normalization
    lbp_features = [(element[1]/float(a*b)) for element in histogram]
    # print len(lbp_features)

    # ####### GLCM ######## #

    distances = [2, 3, 4, 5]
    theta = [0,  np.pi/4,  np.pi/2,  3*np.pi/2,  np.pi]

    glcm = greycomatrix(img_gray, distances, theta, normed=True)
    props = {}
    for prop in [
            'contrast', 'dissimilarity', 'homogeneity', 'energy',
            'correlation', 'ASM'
            ]:
        props[prop] = greycoprops(glcm, prop)
    props['contrast'] /= props['contrast'].max()
    props['dissimilarity'] /= props['dissimilarity'].max()

    glcm_feature = []
    for i in props.keys():
        for d in range(len(distances)):
            for t in range(len(theta)):
                glcm_feature.append(props[i][d][t])

    # print len(glcm_feature)

    return np.hstack([lbp_features, glcm_feature])

