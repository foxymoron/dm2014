#!/usr/bin/env python2.7

import sys

import numpy as np

from sklearn.linear_model.stochastic_gradient import SGDClassifier
from sklearn.kernel_approximation import AdditiveChi2Sampler

# one classifier for the mapper
# this is the classifier on which we'll be running the partial_fit
classifier = SGDClassifier()

# kernel
kernel = AdditiveChi2Sampler(sample_steps=3)

# batch size for the partial_fit
BATCH_SIZE = 50
X_train_batch = np.array([])
Y_train_batch = np.array([])
count = 0


# appended 1 to the original features for centering the data, the
# classifier also calculates the intercept which is appended to
# the weights
def transform(x_original):
    x_transform = kernel.fit_transform(x_original)
    return np.append(x_transform, [1])


# run paritial_fit for the classifier with each picture
def train(y, features):
    classifier.partial_fit(features, y, classes=[1, -1])


if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        data_point = np.fromstring(line, dtype=np.float64, sep=" ")
        features = data_point[1:]

        # if count is zero then no picture has yet been added to the
        # batch. add the first picture to the batch and continue
        if count == 0:
            X_train_batch = kernel.fit_transform(np.array([features]))
            Y_train_batch = np.array(data_point[0])
            count = count + 1
            continue

        # when BATCH_SIZE pictures are available then train the
        # the classifier else keep on adding pictures to the batch
        if count % BATCH_SIZE != 0:
            X_train_batch = np.vstack([X_train_batch, kernel.fit_transform(np.array([features]))])
            Y_train_batch = np.append(Y_train_batch, data_point[0])
            count = count + 1
        else:
            train(Y_train_batch, X_train_batch)
            X_train_batch = np.array([])
            Y_train_batch = np.array([])
            count = 0

    # to take care of the additional pictures which were greater
    # than the last batch size
    if count != 0:
        train(Y_train_batch, X_train_batch)

    temp = classifier.coef_[0]
    # appending intercept to the calculated weights
    temp = np.append(temp, classifier.intercept_)

    value = ' '.join(str(x) for x in temp)

    print '%s\t%s' % ('1', value)
