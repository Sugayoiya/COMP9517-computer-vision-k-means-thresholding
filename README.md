# k-means-thresholding

Python 3+

The following libraries are also available:
OpenCV 3.0+
Numpy, Numba

file structure:

1. k_means_thresholding.{py,cpp}
2. filtered_k_means_thresholding. {py,cpp}
3. step_2.txt
4. count_eggs_4. {py,cpp}

step1:  thresholding of the greyscale image using K-means algorithm

  ● Input: a greyscale image

  ● Output: a binary image

  ● Testing sequence:

    `python3 k_means_thresholding.py input_image_1.jpg output_binary.jpg`

step2: filtering and thresholding of the greyscale image

  ● Input: a greyscale image

  ● Output: a binary image

  ● Testing sequence:

    `python3 filtered_k_means_thresholding.py input_image_1.jpg output_binary.jpg`

step3: partitioning similar neighbourhood pixels in output of Step 2 using connected components

  ● Inputs: a binary image, a positive integer n which is the minimum number of pixels in the component

  ● Outputs: the number of eggs with area larger than n pixels in the image written to stdout AND write a colour image to ./output_eggs.jpg where each egg found is a different colour.

  ● Testing sequence:
    `python3 count_eggs_4.py 50 output_binary.jpg labeled.jpg`

input image:

![alt text](https://github.com/mokomokoo/COMP9517-computer-vision-k-means-thresholding/blob/master/input_image_1.jpg)

grey image (after step 1):

![alt text](https://github.com/mokomokoo/COMP9517-computer-vision-k-means-thresholding/blob/master/output_binary.jpg)

labeled image:

![alt text](https://github.com/mokomokoo/COMP9517-computer-vision-k-means-thresholding/blob/master/labeled.png)
