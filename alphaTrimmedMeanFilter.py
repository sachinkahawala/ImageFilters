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

# calculating value for the given i, j points
# time complexity O(window_size**2 * log (window_size**2))
def calValue(im, i, j, w, alpha):
    A=im[i-w/2:i+w/2+1, j-w/2:j+w/2+1].flatten()
    A.sort()
    if alpha:B=A[alpha/2:-alpha/2]
    else:B=A
    return int(np.mean(B))

# applying alpha trimmed mean filter for the given image matrix
# time complexity O (width*height*window_size**2 * log (window_size**2))
def applyFilter(im, n, m, w, alpha):
    newImage, nH, nW = corrrectEdges(im, n, m, w)
    newImageFinal=deepcopy(newImage)
    for i in range(n):
        for j in range(m):
            newImageFinal[i+w/2][j+w/2]=calValue(newImage,i+w/2,j+w/2,w,alpha)
    return newImageFinal[w/2:-w/2+1,w/2:-w/2+1]


start=time.time()
# input image
img = Image.open('image3.jpg')
img.show()
# Dividing into rgb channels
arr = np.array(img)
red = arr[:,:,2]
green = arr[:,:,1]
blue = arr[:,:,0]
h,wi=len(red),len(red[0])

# Window size and alpha
w=3
alpha=4
# calculating filterd red matrix
Rn=np.array(applyFilter(red,h,wi,w,alpha)).astype(np.uint8)
# calculating filterd green matrix
Gn=np.array(applyFilter(green,h,wi,w,alpha)).astype(np.uint8)
# calculating filterd blue matrix
Bn=np.array(applyFilter(blue,h,wi,w,alpha)).astype(np.uint8)
# combining 3 matrixes
rgb = np.dstack((Bn,Gn,Rn))
# Final image
img = Image.fromarray(rgb, 'RGB')
img.show()
img.save('alphaMeanFilterdImage6.png')
print time.time()-start
