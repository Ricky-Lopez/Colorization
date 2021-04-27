import queue
import random
import math
import time
import copy
import operator
from collections import Counter
from math import sqrt
from random import randint
from PIL import Image


class patchData:
     def __init__(self, position, patch, middle) : 
        self.position = position #Holds the position of the patch
        self.patch = patch #Holds the 3X3 patch
        self.middle = middle #Holds the middle pixel of the 3X3 patch
        
#Returns a 9 value list/vector that represent the patch for a given pixel
def getPatch(px, position):
    
    patch = []
    
    #grabs the position of the pixel
    i = position[0]
    j = position[1]
    
    grayValue = px[i-1,j-1][0] #used for debugging 
    
    #Goes through the 3X3 patch and collects the 9 grey values
    patch.append(px[i-1,j-1][0])
    patch.append(px[i,j-1][0])
    patch.append(px[i+1,j-1][0]) 
    patch.append(px[i-1,j][0])
    patch.append(px[i,j][0]) 
    patch.append(px[i+1,j][0])
    patch.append(px[i-1,j+1][0])
    patch.append(px[i,j+1][0])
    patch.append(px[i+1,j+1][0])
    
    #returns the 9 value list/vector 
    return patch
    
#Used for the training image to make looking for similar patches quicker 
def setPatchData(px, width, height):
    
    patchDataList = []
    
    for i in range(width):
        for j in range(height):
            
            patch = []
            
            #Makes sure the pixel isn't on the edge
            if(i != 0 and j != 0 and i != (width - 1) and j != (height - 1)): 
               
                patch = getPatch(px, [i,j]) #gets the patch for the given pixel
                dataHolder = patchData( [i,j], patch, px[i,j][0])

                patchDataList.append(dataHolder)
    
    #Returns a list of patch data for each pixel         
    return patchDataList

def basicAgent(training_img, testing_img, recolored_training_img):
    
    width, height = testing_img.size
    testing_px = testing_img.load()
    training_px = training_img.load()
    recolored_px = recolored_training_img.load()
    
    #Sets all the training image pixels to make looking for similar patches more efficient
    training_patchDataList = setPatchData( training_px, width, height)
    
    
    print('Total pixels: ', ((width * height) - (width * 2) - (height * 2))) #used for testing
    
    index = 0
    userCounter = 0
    
    for i in range(width):
        for j in range(height):
            
            #If the pixel is on the edge, just color it black
            if(i == 0 or j == 0 or i == (width - 1) or j == (height - 1)):
                testing_px[i,j] = (0,0,0)
            else:
            
                patch = getPatch(testing_px, [i,j]) # Grabs the patch of the current pixel
                #Grabs the six most similar patch data to the current  testing patch
                sixSimilar = searchSimilar(patch, training_patchDataList) 
                #Gets the majority representative color of the six similar training patches
                color = getColorRepresent(sixSimilar, recolored_px)
                #recolors the testing pixel to the color
                testing_px[i,j] = color
                
                #Used for testing to see what pixel its on
                userCounter += 1
                index += 1
                if(userCounter == 100) :
                    userCounter = 0
                    print('index at: ', index)
                
    testing_img.save("image_process/reconstructed.jpg")
    
    combine_image(recolored_training_img, testing_img).save("image_process/full_reconstructed.jpg")
    
#Returns a majority representative color using the given six similar patches
def getColorRepresent(sixSimilar, recolored_px):
    
    colors = []
    
    for i in range(len(sixSimilar)):
        
        #Grabs the current patch location (the pixel location)
        location = sixSimilar[i].position
        x = location[0]
        y = location[1]
        #Gets the color of the pixel in the recolored image
        colors.append(recolored_px[x,y])
    
    common = Most_Common(colors) # Gets the most common color of the list
    
    return common

#Class used to efficiently compare the patch and its distance to the testing patch
class compareData:
    def __init__(self, distance, patchData):
        self.distance = distance #holds the Euclidean distance to the current testing patch
        self.patchData = patchData #holds the training patch data
    
#returns the six most similar 3X3 grayscale pixel patched in the training data to a given testing patch
def searchSimilar(patch, training_patchDataList): 
    
    distances = []
    
    for i in range(len(training_patchDataList)):
        
        trainingPatch = training_patchDataList[i].patch #gets the current training patch
        #using Euclidean distance to compare the current training patch to the current testing patch 
        distance = calcEuclideanDistance(patch, trainingPatch) 
        #Defines a compare data object for the current training patch
        compare = compareData(distance,training_patchDataList[i])
        
        distances.append(compare)
    
    #Sorts all the distances of the training patches 
    sorted_distances = sorted(distances, key=operator.attrgetter("distance"))
    
    #Gets the six smallest distances to the current testing patch (the six most similar 3#3 grayscale pixel patch)
    topSix = [sorted_distances[0].patchData, sorted_distances[1].patchData, sorted_distances[2].patchData, 
              sorted_distances[3].patchData, sorted_distances[4].patchData ,sorted_distances[5].patchData]
    
    return topSix
    
    
# Calculates the Euclidean distance of a testing patch/vector to a training patch/vector to compare similarities
def calcEuclideanDistance(vectorOne, vectorTwo):
    
    sum = 0
    for i in range(len(vectorOne)):
        result = (vectorOne[i] - vectorTwo[i])**2
        sum = sum + result
        
    return sqrt(sum)

#Returns the most common color of the list
def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]

#combines two images into one horizontally
def combine_image(imageOne, imageTwo):
    new = Image.new('RGB', (imageOne.width + imageTwo.width, min(imageOne.height, imageTwo.height)))
    new.paste(imageOne, (0, 0))
    new.paste(imageTwo, (imageOne.width, 0))
    return new
    
    