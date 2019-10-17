import cv2,random,sys,os,numpy as np

def filter_k_means():  
    
    if len(sys.argv) != 3:
        print('please input correct arguments')
        print('exmaple: python k_means_thresholding.py input.jpg output_binary.jpg ')
        sys.exit()
    else:
        # for arg in sys.argv:
        #     print(arg)
        if not os.path.exists(sys.argv[1]):
            print('input picture dose not exit!')
            sys.exit()

        image = cv2.imread(sys.argv[1],0)

        # kernel
        kernel = np.ones((5,5),np.uint8)
        # closing
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        
        # cv2.imshow('image',image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        height,width = image.shape
        # print(image,'height:',height,'width:',width)

        c1 = random.randint(0,255)  # cluster 1
        c2 = random.randint(0,255)  # cluster 2

        # print('cluster:',c1,c2,'middle:',(c2+c1)//2)
        middle = (c2+c1)//2

        cluster = np.zeros(image.shape)
        cluster[image > middle] = 2
        cluster[image <= middle] = 1

        clu1 = 0
        clu2 = 0

        for i in range(height):
            for j in range(width):
                if cluster[(i,j)] == 1:
                    clu1 += image[(i,j)]
                else:
                    clu2 += image[(i,j)]

        unique, counts = np.unique(cluster,return_counts = True)
        L = dict(zip(unique,counts))

        # if all in cluster 1 or cluster 2
        if len(L) != 2:
            for i in L.items():
                if i[0] == 1.0:
                    L[2.0] = 0
                    clu1 = clu1//L[1.0]
                    clu2 = 0
                    break
                else:
                    L[1.0] = 0
                    clu1 = 0
                    clu2 = clu2//L[2.0]
                    break
        else:
            clu1 = clu1//L[1.0]
            clu2 = clu2//L[2.0]

        # print('calculated cluster point:',clu1,clu2,'\n')

        while clu1 != c1 or clu2 != c2:
            # print('while started!\n')
            c1 = clu1
            c2 = clu2
            # print(c1,c2)
            middle = (c1+c2)//2
            # print('middle:',middle,'\n')
            cluster[image > middle] = 2
            cluster[image <= middle] = 1
            
            clu1 = 0
            clu2 = 0

            for i in range(height):
                for j in range(width):
                    if cluster[(i,j)] == 1:
                        clu1 += image[(i,j)]
                    else:
                        clu2 += image[(i,j)]

            unique, counts = np.unique(cluster,return_counts = True)
            L = dict(zip(unique,counts))

            # if all in cluster 1 or cluster 2
            if len(L) != 2:
                for i in L.items():
                    if i[0] == 1.0:
                        L[2.0] = 0
                        clu1 = clu1//L[1.0]
                        clu2 = 0
                        break
                    else:
                        L[1.0] = 0
                        clu1 = 0
                        clu2 = clu2//L[2.0]
                        break
            else:
                clu1 = clu1//L[1.0]
                clu2 = clu2//L[2.0]
            # print('calculated cluster point:',clu1,clu2)

        # print(cluster)
        # set pic to binary pic
        image[cluster == 2] = 255
        image[cluster == 1] = 0

        return image



if __name__ == "__main__":
    img = filter_k_means()
    cv2.imwrite(sys.argv[2],img)
    # cv2.imshow('image',image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()