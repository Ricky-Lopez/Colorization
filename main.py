import queue
import random
import math
import time
import copy
import basicAgent
import advancedAgent as aa
from random import randint
from PIL import Image
from copy import deepcopy

#K means for image averaging.
def k_means(pxLoad, width, height, k) :
    print("Clustering . . . (This may take a while!)")

    #initialization
    averages = []
    clAvg = []
    for i in range(k):
        clAvg.append([0,0])
    currLowestProximity = 2147483647
    sameAvgCounter = 0
    clusterLoopCounter = 0
    userCounter = 0

    #ensures that every pixel chosen for the start of the cluster is different. 
    while( not(noDup(clAvg)) ) :
        for i in range(k):
            clAvg[i] = [randint(0, width) , randint(0, height)]

    for i in range(k):
        averages.append(pxLoad[clAvg[i][0], clAvg[i][1]])

    
    #keeps iterating until the average color of each cluster no longer changes. 
    while(not(sameAvgCounter == (k-1))) :
        
        userCounter += 1
        if(userCounter == 15) :
            userCounter = 0
            print("Still clustering . . .")
    

        sameAvgCounter_old = sameAvgCounter
        sameAvgCounter = 0
        clusters = []
        for i in range(k):
            clusters.append([])

        #Iterates through all pixels, adding them to their respective cluster.
        for i in range(width):
            for j in range(height):
                for l in range(len(averages)):
                    proximityRed = abs(averages[l][0] - pxLoad[i,j][0])
                    proximityGreen = abs(averages[l][1] - pxLoad[i,j][1])
                    proximityBlue = abs(averages[l][2] - pxLoad[i,j][2])
                    proximity = math.sqrt((proximityRed ** 2) + (proximityGreen ** 2) + (proximityBlue ** 2))
                    if(proximity < currLowestProximity):
                        currLowestProximity = proximity
                        cluster = l
                
                clusters[cluster].append(px[i,j])
                currLowestProximity = 2147483647
        
        #Calculate the average of each of the clusters and overwrite them. If all cluster averages have stayed the same, return averages. 
        for i in range(len(clusters)) :
            #print(len(clusters[i]))
            redAvg = 0
            greenAvg = 0
            blueAvg = 0
            for j in range(len(clusters[i])) :
                redAvg = redAvg + clusters[i][j][0]
                greenAvg = greenAvg + clusters[i][j][1]
                blueAvg = blueAvg + clusters[i][j][2]

            if( len(clusters[i]) ) :
                redAvg = redAvg / len(clusters[i])
                greenAvg = greenAvg / len(clusters[i])
                blueAvg = blueAvg / len(clusters[i])


            if(averages[i] == (int(redAvg), int(blueAvg), int(greenAvg))) :
                sameAvgCounter = sameAvgCounter + 1

            if( len(clusters[i]) ) : #If there were items in the cluster, then use cluster information and change cluster average.
                averages[i] = (int(redAvg), int(blueAvg), int(greenAvg))
            else:
                sameAvgCounter = sameAvgCounter + 1
        
        #CLUSTER LOOP PREVENTION. If cluster averages teeter between numbers for too long, algorithm will terminate.
        if(sameAvgCounter == sameAvgCounter_old) :
            clusterLoopCounter += 1
        else:
            clusterLoopCounter = 0
        if(clusterLoopCounter > 30):
            print(averages)
            return averages

        #print("Clusters Stabilized: " , sameAvgCounter)
    
    print(averages)
    return averages

#helper function for k_means.
def noDup(list) :
    for i in range(len(list)) :
        for j in range(len(list)) :
            if(not(i == j)) :
                if(list[i] == list[j]) :
                    return False
    return True
    

if __name__ == '__main__' :

    img = Image.open("image_process/image.jpg") #Full Image
    width, height = img.size

    #Creation of Training Data and Testing Data
    left_half = (0, 0, width/2, height) #Area tuple of left half
    right_half = (width/2, 0, width, height) #Area tuple of right half

    testing_img_C = img.crop(right_half)
    training_img_C = img.crop(left_half)
    testing_img_C.save("image_process/testing_data_COLOR.jpg")
    training_img_C.save("image_process/training_data_COLOR.jpg")
    px_testing_data = testing_img_C.load()

    #Grayscale Code
    px = img.load()
    for i in range(width):
        for j in range(height):
            avg = (px[i,j][0] + px[i,j][1] + px[i,j][2]) / 3
            px[i,j] = (int(avg), int(avg), int(avg))
    img.save("image_process/image_grayscale.jpg")

    testing_img = img.crop(right_half)
    training_img = img.crop(left_half)
    testing_img.save("image_process/testing_data.jpg")
    training_img.save("image_process/training_data.jpg")

    img = Image.open("image_process/image.jpg")
    px = img.load()
    k = int(input("Please enter the number of colors you would like to average the image into: "))
    colors = k_means(px, width, height, k) #k_means to determine the 5 colors.

    #Replacing the true colors of the left half of the image with the 5 colors.

    recolored_training_img = training_img.copy()
    width, height = recolored_training_img.size
    px_recolored_training = recolored_training_img.load()

    #reinitializes every pixel on the left side of the image.
    for i in range(width):
        for j in range(height):
            lowestProx = 2147483647
            for k in range(len(colors)) :
                redProx = abs(px[i,j][0] - colors[k][0])
                greenProx = abs(px[i,j][1] - colors[k][1])
                blueProx = abs(px[i,j][2] - colors[k][2])
                trueProx = math.sqrt( (redProx ** 2) + (greenProx ** 2) + (blueProx **2) )

                if(trueProx < lowestProx) :
                    px_recolored_training[i,j] = colors[k]
                    lowestProx = trueProx
                

    #basicAgent.basicAgent(training_img, testing_img, recolored_training_img)

    learningRate = float(input("what should the learning rate be?"))
    aa.advancedAgent(training_img_C, testing_img, training_img)

    #restructuring the new final image

    colorized = Image.open("image_process/testing_img_COLORIZED.jpg")

    left_size = training_img_C.size
    right_size = colorized.size

    new_image = Image.new('RGB' , (2*left_size[0], left_size[1]), (250,250,250) )
    new_image.paste(training_img_C, (0,0))
    new_image.paste(colorized, (left_size[0], 0))
    new_image.save("image_process/FINAL_IMAGE.JPG")
    new_image.show()






    #Accuracy Analysis
    '''


    recolored_testing_img = testing_img.copy()
    width, height = recolored_testing_img.size
    px_recolored_testing = recolored_testing_img.load()

    for i in range(width):
        for j in range(height):
            lowestProx = 2147483647
            for k in range(len(colors)) :
                redProx = abs(px_testing_data[i,j][0] - colors[k][0])
                greenProx = abs(px_testing_data[i,j][1] - colors[k][1])
                blueProx = abs(px_testing_data[i,j][2] - colors[k][2])
                trueProx = math.sqrt( (redProx ** 2) + (greenProx ** 2) + (blueProx **2) )

                if(trueProx < lowestProx) :
                    px_recolored_testing[i,j] = colors[k]
                    lowestProx = trueProx

    recolored_testing_img.save("image_process/TRUE_COLOR.jpg")
    '''
                
    



