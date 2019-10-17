import cv2,random,os,sys,numpy as np
from collections import defaultdict


def count_eggs():  
    
    if len(sys.argv) != 4:
        print('please input correct arguments')
        print('exmaple: python count_eggs_4.py binary_image.jpg n output_eggs.jpg  ')
        sys.exit()
    else:
        if not os.path.exists(sys.argv[1]):
            print('input picture dose not exit!')
            sys.exit()

        image = cv2.imread(sys.argv[1],0)

        #image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]
        image[image<=127] = 0
        image[image>127] = 255

        image_padding = np.ones((image.shape[0]+2,image.shape[1]+2))
        image_padding*255
        image_padding[1:-1,1:-1] = image

        L = [] # labels
        image_padding[image_padding == 1] = 255
        # print(image_padding)
        label = np.zeros_like(image_padding)

        # find neighbours
        def get_neighbour(i,j,con):
        #     print(i,j,type(i),type(j))
        #     print('find neighbours now...')
            neighbours = []
            
            up = i - 1
            down = i + 1
            left = j - 1
            right = j + 1
            
            con_4 = [(up,j),(i,left),(i,right),(down,j)]
            con_8 = [(up,left),(up,j),(up,right),(i,left),(i,right),(down,left),(down,j),(down,right)]
            
            if con == 4:
                for i in con_4:
                    if image_padding[i] != 255 and label[i] != 0:
                        neighbours.append(i)
            elif con == 8:
                for i in con_8:
                    if image_padding[i] != 255 and label[i] != 0:
                        neighbours.append(i)
            return neighbours

        # background 255
        height, width = image.shape
        linked = defaultdict(set)
        nextlabel = 1.0

        # first pass:
        for i in range(1,height+1):
            for j in range(1,width+1):
        #         print('point:',(i,j))
                if image_padding[i,j] != 255:
                    neighbours = get_neighbour(i,j,4)
                    if len(neighbours) == 0:
                        linked[nextlabel].add(nextlabel)
                        label[i,j] = nextlabel
                        nextlabel += 1
                    else:
                        L = [label[p] for p in neighbours]
                        label[i,j] = min(L)
                        for labels in list(set(L)):
                            for labels_ in list(set(L)):
                                linked[labels].add(labels_)

        # label is calculated

        # calculate equivalent label
        equivalent = list()

        for i in linked:
        #     print(linked[i])
            equivalent.append(list(linked[i]))
            
        out = [] 
        while len(equivalent)>0:
            first, rest = equivalent[0], equivalent[1:]
            first = set(first)

            lf = -1
            while len(first)>lf:
                lf = len(first)

                rest2 = []
                for r in rest:
                    if len(first.intersection(set(r)))>0:
                        first |= set(r)
                    else:
                        rest2.append(r)     
                rest = rest2

            out.append(first)
            equivalent = rest
        
        countlabel = 1
        output = defaultdict(list) # equivalent label list
        for i in out:
            output[countlabel] = i
            countlabel += 1
        
        # find labels
        def find_labels(label):
            for i in output:
                if label in output[i]:
                    return i
        
        # second pass
        for i in range(1,height+1):
            for j in range(1,width+1):
                if image_padding[i,j] != 255:
                    label[i,j] = find_labels(label[i,j])

        # print(np.max(label))

        # count pixels
        unique, counts = np.unique(label, return_counts = True)
        a = dict(zip(unique,counts))
    
        right = [i for i in a if a[i]> int(sys.argv[2])][1:]

        faker = np.zeros_like(label)*255
        countt = 1 
        for i in right:
            faker[label == i] = countt
            countt += 1
            
        # number of eggs counted
        print(int(np.max(faker)))

        faker = faker[1:-1,1:-1] # remove padding 
        # Map component labels to hue val
        label_hue = np.uint8(179*faker/np.max(faker))
        blank_ch = 255*np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

        # cvt to BGR for display
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

        # set bg label to black
        labeled_img[label_hue==0] = 255
        return labeled_img



if __name__ == "__main__":
    img = count_eggs()
    # cv2.imshow(sys.argv[3], labeled_img)
    cv2.imwrite(sys.argv[3],img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()