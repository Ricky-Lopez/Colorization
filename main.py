import queue
import random
import math
import time
import copy
from random import randint
from PIL import Image

#K means with K set to 5.
def k_means(pxLoad, width, height) :

    #initialization
    averages = []
    clusters = [ [], [], [], [], [] ]
    clAvg1 = [0,0]
    clAvg2 = [0,0]
    clAvg3 = [0,0]
    clAvg4 = [0,0]
    clAvg5 = [0,0]
    currLowestProximity = width + height
    sameAvgCounter = 0

    #ensures that every pixel chosen for the start of the cluster is different. 
    while(clAvg1 == clAvg2 or clAvg1 == clAvg3 or clAvg1 == clAvg4 or clAvg1 == clAvg5 or clAvg2 == clAvg3 or clAvg2 == clAvg4 or clAvg2 == clAvg5 or clAvg3 == clAvg4 or clAvg3 == clAvg5 or clAvg4 == clAvg5) :
        clAvg1 = [randint(0, width) , randint(0, height)]
        clAvg2 = [randint(0, width) , randint(0, height)]
        clAvg3 = [randint(0, width) , randint(0, height)]
        clAvg4 = [randint(0, width) , randint(0, height)]
        clAvg5 = [randint(0, width) , randint(0, height)]
    
    averages.append(pxLoad[clAvg1[0], clAvg1[1]])
    averages.append(pxLoad[clAvg2[0], clAvg2[1]])
    averages.append(pxLoad[clAvg3[0], clAvg3[1]])
    averages.append(pxLoad[clAvg4[0], clAvg4[1]])
    averages.append(pxLoad[clAvg5[0], clAvg5[1]])
    
    #keeps iterating until the average color of each cluster no longer changes. 
    while(not(sameAvgCounter == 5)) :
        sameAvgCounter = 0
        #Iterates through all pixels, adding them to their respective cluster.
        for i in range(width):
            for j in range(height):
                for k in range(len(averages)):
                    proximityRed = math.sqrt((averages[k][0] - pxLoad[i,j][0]) ** 2)
                    proximityGreen = math.sqrt((averages[k][1] - pxLoad[i,j][1]) ** 2)
                    proximityBlue = math.sqrt((averages[k][2] - pxLoad[i,j][2]) ** 2)
                    proximity = math.sqrt((proximityRed + proximityGreen + proximityBlue) ** 2)
                    if(proximity <= currLowestProximity):
                        currLowestProximity = proximity
                        cluster = k

                clusters[cluster].append(px[i,j])
        
        #Calculate the average of each of the clusters and overwrite them. If no cluster averages have been overwritten 

        for i in range(len(clusters)) :
            redAvg = 0
            greenAvg = 0
            blueAvg = 0
            for k in range(len(clusters[i])) :
                redAvg += clusters[i][k][0]
                greenAvg += clusters[i][k][1]
                blueAvg += clusters[i][k][2]
            
            redAvg = redAvg / len(clusters[i])
            greenAvg = greenAvg / len(clusters[i])
            blueAvg = blueAvg / len(clusters[i])
            if(averages[i] == [int(redAvg), int(blueAvg), int(greenAvg)]) :
                sameAvgCounter = sameAvgCounter + 1
            averages[i] = [int(redAvg), int(blueAvg), int(greenAvg)]
        
        print(sameAvgCounter)
    
    return averages

            
    

if __name__ == '__main__' :

    img = Image.open("image_0.jpg") #Full Image
    width, height = img.size

    #Grayscale Code#
    px = img.load()
    for i in range(width):
        for j in range(height):
            avg = (px[i,j][0] + px[i,j][1] + px[i,j][2]) / 3
            px[i,j] = (int(avg), int(avg), int(avg))
    img.save("image_0_grayscale.jpg")

    #Creation of Training Data and Testing Data#
    left_half = (0, 0, width/2, height) #Area tuple of left half
    right_half = (width/2, 0, width, height) #Area tuple of right half
    testing_img = img.crop(right_half)
    training_img = img.crop(left_half)
    testing_img.save("testing_data.jpg")
    training_img.save("training_data.jpg")

    colors = k_means(px, width, height)