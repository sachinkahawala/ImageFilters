from copy import copy, deepcopy
import numpy as np
from PIL import Image
import time

# im - Image 2D array
# n  - Height of the image
# m  - Width of the image
# w  - Window size

# replicate padding has beign implemented
# time complexity O(max(height*window_size,width*window_size))
# for a image matrix of [1,2,3]
#                       [4,5,6]
# padded matrix for a window size 3 will be
#     [1,1,2,3,3]
#     [1,1,2,3,3]
#     [4,4,5,6,6]
#     [4,4,5,6,6]
def corrrectEdges(im, n, m, w):
    newImage = [[-1]*(m+(w/2)*2) for _ in range((n+(w/2)*2))]
    for i in range(n):
        for j in range(m):
            newImage[i+w/2][j+w/2]=im[i][j]
    nH,nW=len(newImage),len(newImage[0])
    for i in range(0,w/2):
        for j in range(nW):
            newImage[i+n+w/2][j]=newImage[i+n+w/2-1][j]
    for i in range(w/2-1,-1,-1):
        for j in range(nW):
            newImage[i][j]=newImage[i+1][j]
    for i in range(nH):
        for j in range(0,w/2):
            newImage[i][j+m+w/2]=newImage[i][j+m+w/2-1]
    for i in range(nH):
        for j in range(w/2-1,-1,-1):
            newImage[i][j]=newImage[i][j+1]
    return (np.array(newImage), nH, nW)

# calculates the loacl mean matrix of the given image matrix
# time complexity O (width*height*window_size**2)
def localMean(im, n, m, w):
    lMean=deepcopy(im)
    lMean=lMean.astype(np.float32)
    for i in range(n):
        for j in range(m):
            I,J=i+w/2,j+w/2
            lMean[I][J]=np.mean(im[I-w/2:I+w/2+1, J-w/2:J+w/2+1])
    return lMean[w/2:-w/2+1,w/2:-w/2+1]

# calculates the varianceOfNoice Into localVariance matrix for the given image matrix
# time complexity O (width*height*window_size**2)
def varianceOfNoiceIntolocalVariance(im, n, m, w, noiceVariance):
    lVariance=deepcopy(im)
    lVariance=lVariance.astype(np.float32)
    for i in range(n):
        for j in range(m):
            I,J=i+w/2,j+w/2
            lVariance[I][J]=np.var(im[I-w/2:I+w/2+1, J-w/2:J+w/2+1])
    lVariance=lVariance[w/2:-w/2+1,w/2:-w/2+1]
    # varince of noice is assumed as mean of local variance
    varianceOfNoice=noiceVariance#np.mean(lVariance)
    for i in range(n):
        for j in range(m):
            if varianceOfNoice>lVariance[i][j]:
                lVariance[i][j]=varianceOfNoice

    return varianceOfNoice/lVariance

# applying adaptive filter for the given image matrix
# time complexity O (width*height*window_size**2)
def applyFilter(im, n, m, w,noiceVariance):
    newImage, nH, nW = corrrectEdges(im, n, m, w)
    im=np.array(im).astype(np.float32)
    finalImage=(im - varianceOfNoiceIntolocalVariance(newImage,n,m,w,noiceVariance)*(im-localMean(newImage,n,m,w))).astype(np.uint8)

    return finalImage


start=time.time()
# input image
img = Image.open('image3.jpg')
img.show()
arr = np.array(img)
# Dividing into rgb channels
red = arr[:,:,2]
green = arr[:,:,1]
blue = arr[:,:,0]
# height and width of image
h,wi=len(red),len(red[0])

# window size
w = 3
noiceVariance=1
# calculating filterd red matrix
Rn=np.array(applyFilter(red,h,wi,w,noiceVariance))
# calculating filterd green matrix
Gn=np.array(applyFilter(green,h,wi,w,noiceVariance))
# calculating filterd blue matrix
Bn=np.array(applyFilter(blue,h,wi,w,noiceVariance))
# combining 3 matrixes
rgb = np.dstack((Bn,Gn,Rn))
# Final image
img = Image.fromarray(rgb, 'RGB')
img.show()
img.save('adaptiveFilteredImage5.png')
print time.time()-start
