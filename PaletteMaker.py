import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from skimage import io
from sklearn.utils import shuffle
from time import time

corner_values = np.array([[255,255,255], [0,0,0], [0,255,255], [255,0,255], [255,255,0], [0,0,255], [255,0,0], [0,255,0]] , dtype=np.uint8)

def getPalette(imagepath, bitdepth):
    bits = bitdepth
    imagename = imagepath
    n_colors = 1 << bits

    image = io.imread((os.getcwd() + imagename))
    #imageFloated = np.array(image, dtype=np.float64)/255
    imageArrayed = np.array(image, dtype=np.uint8)

    w, h, d = tuple(imageArrayed.shape)
    assert d == 3
    image_array = np.reshape(imageArrayed,(w * h, d))
    print("Fitting model  and labels on a small sub-sample of the data")
    t0 = time()
    image_array_sample = shuffle(image_array, random_state=0, n_samples=64)
    kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
    print(f"done in {time() - t0:0.3f}s.")

    return(kmeans.cluster_centers_)

def pruneBlackAliases(unrolled_image):
    #print("Curating dataset to remove perceptually identical black pixels")
    pruned = np.ndarray(shape=(0,3))
    for i, pixel in enumerate(unrolled_image):
        if ( pixel[0] > 35 and pixel[1] > 35 and pixel[2] > 35):
            pruned = np.append( pruned, pixel.reshape(1,3), axis=0)
            #print("Wrote pixel #" + str(i))

    return pruned
            
def injectGrayScale(unrolled_image, grayfraction, graybands):
    dankimage = unrolled_image
    
    totpix = unrolled_image.size            
    print(totpix)

    graypix = totpix * grayfraction
    bandsize = int(graypix/graybands)

    for i in range(graybands):
        grayness = (255/graybands * i)
        appendy = np.ndarray(shape=(bandsize,3), dtype=np.uint8)
        appendy.fill(grayness)
        dankimage = np.append(dankimage, appendy, axis=0)
        
    return dankimage

def getPaletteMultiImage(parentDir, bitdepth, samplect):

    bits = bitdepth
    imagePath = parentDir
    n_colors = 1 << bits
    image_unrolled = np.ndarray(shape=(0,3))

    for filename in os.listdir(parentDir):
        image = io.imread((parentDir + filename))
        imageArrayed = np.array(image, dtype=np.uint8)
        w, h, d = tuple(imageArrayed.shape)
        assert d == 3
        toAppend = np.reshape(imageArrayed,(w * h, d))
        image_unrolled = np.vstack((image_unrolled, toAppend))

    print("Fitting model  and labels on a small sub-sample of the data")
    t0 = time()
    image_array_sample = shuffle(image_unrolled, random_state=0, n_samples=samplect)
    image_array_sample = pruneBlackAliases(image_array_sample)
    image_array_sample = injectGrayScale(image_array_sample, .5, 32)
    kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
    print(f"done in {time() - t0:0.3f}s.")

    return(kmeans)

def recreate_image(targetPath, kmeans):
    t0 = time()
    image = io.imread((os.getcwd() + targetPath))
    imageIntegerized = np.array(image, dtype=np.uint8)
    w, h, d = tuple(imageIntegerized.shape)
    image_unrolled = np.reshape(imageIntegerized, (w * h, d))

    t1 = time()
    labels = kmeans.predict(image_unrolled)
    codebook = kmeans.cluster_centers_
    output = codebook[labels].reshape(w, h, -1)
    outputIntegerized = np.array(output, dtype=np.uint8)
    print(f"Frame generated in {time() - t0:0.3f}s.")
    print(f"Prediction took {time() - t0:0.3f}s.")

    return outputIntegerized 