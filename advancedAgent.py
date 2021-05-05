import queue
import random
import math
import time
import copy
import basicAgent
from random import randint
import numpy as np
from PIL import Image
from copy import deepcopy

def advancedAgent(training_img, testing_img, grayscale_training_img):

    #STEP 1: TRAINING DATA REFACTORING

    tr_px = training_img.load()
    gs_tr_px = grayscale_training_img.load()
    width, height = training_img.size
    
    red_output_data = []
    green_output_data = []
    blue_output_data = []

    gray_input_data = createVectors(gs_tr_px, width, height, 0) #any color used for color flag is fine, as each color holds the same value in grayscale.
    
    for i in range(width-2):
        for j in range(height-2):
            red_output_data.append(rescaleData2(tr_px[(i+1),(j+1)][0]))
            green_output_data.append(rescaleData2(tr_px[(i+1),(j+1)][1]))
            blue_output_data.append(rescaleData2(tr_px[(i+1),(j+1)][2]))

    
    randValue = randint(0, len(gray_input_data))


    #STEP 2: ADD FEATURES TO INPUT DATA (OPTIONAL DEPENDING ON MODEL!)

    #gray_input_data = addFeatures(gray_input_data, 0)


    #STEP 3: CONSTRUCT WEIGHT VECTORS (w0x0 + w1x1 ... wNxN) (begin with unit vector!)

    red_weights = []
    green_weights = []
    blue_weights = []
    for i in range(len(gray_input_data[0])):
        red_weights.append(1) #begin with unit vectors
        green_weights.append(1)
        blue_weights.append(1)


    #STEP 4-6: REGRESSION???? (3 for each color value!)

    print("Regression on red values. . .")
    red_weights_FINAL = logisticRegression(gray_input_data, red_weights, red_output_data)
    
    
    print("Regression on green values. . .")
    blue_weights_FINAL = logisticRegression(gray_input_data, green_weights, blue_output_data)

    print("Regression on blue values. . .")
    green_weights_FINAL = logisticRegression(gray_input_data, blue_weights, green_output_data)
    


    #STEP 7: APPLY WEIGHTS TO RIGHT SIDE OF IMAGE VALUES AND CONVERT BACK TO COLOR VALUES


    tst_px = testing_img.load()
    width, height = testing_img.size

    tester_vector = createVectors(tst_px, width, height, 0)

    red_values = applySigmoidModel(tester_vector, red_weights_FINAL)
    green_values = applySigmoidModel(tester_vector, green_weights_FINAL)
    blue_values = applySigmoidModel(tester_vector, blue_weights_FINAL)

    for i in range(len(red_values)): #conversion back to RGB.
        red_values[i] = round( rescaleDataBack2(red_values[i]))
        green_values[i] = round( rescaleDataBack2(green_values[i]))
        blue_values[i] = round( rescaleDataBack2(blue_values[i]))

    

    #STEP 8: USE VALUES TO CHANGE TEST IMAGE

    colorizeImage(red_values, green_values, blue_values, testing_img, width, height)
    

        

#given the input data, the vector of weights, and the expected output data for training, applies regression on the weight vector.
#stops when TODO: (when does it stop lmfao)
def logisticRegression(input_data, weight_vector, expected_output_data):

    #STEP 4: APPLY MODEL TO INPUT DATA (input_data[i] dot product weight_vector)
    #STEP 5: APPLY LOSS FUNCTION USING PREDICTED DATA AND TRAINING DATA
    #STEP 6: DERIVATIVE MAGIC AND STOCHASTIC GRADIENT DESCENT TO GET NEW WEIGHTS???

    

    for i in range(100): #WHEN DOES IT STOP
        print("On iteration: ", i)
        
        
        predicted_output_data = applySigmoidModel(input_data, weight_vector)

        derivatives = calculateDerivatives(predicted_output_data, expected_output_data, weight_vector, input_data)

        weight_vector = updateWeights(weight_vector, derivatives)

        

    return weight_vector

#DEPRECATED DO NOT USE#################
#modifies an integer (preferably the color value lol) so that instead of having a domain/range of 0->255, they have a range of -1->1 . 
#returns rescaled value
def rescaleData(x):
    y = 1 - (x / 127.5)
    return y 

#function to scale data back to its original form.
#returns scaled value
def rescaleDataBack(x) :
    y = (1 - x) * 127.5
    return y
#DEPRECATED DO NOT USE#################

#alternate function to rescale data because the other one did not make sense
#returns rescaled value
def rescaleData2(x):
    y = x / 255
    return y

#alternate function to rescale data back because the original scaling did not make sense
#returns rescaled value
def rescaleDataBack2(x):
    y = x * 255
    return y

#creates output vectors and stores them into a list. Color flag 0 denotes the red value list, 1 denotes the green value list, 2 denotes the blue value list.
#Also handles rescaling of original color value from 0-255 to 0-1.
#returns list of vectors. 
def createVectors(tr_px, width, height, color_flag):
    data = []
    
    if(color_flag == 0): #Color is red
        color = 0
    elif(color_flag == 1): #Color is green
        color = 1
    elif(color_flag == 2): #Color is blue
        color = 2

    for i in range(width-2):
        for j in range(height-2):
            vector = [1]
            vector.append(rescaleData2(tr_px[(i),(j)][color]))
            vector.append(rescaleData2(tr_px[(i+1),(j)][color]))
            vector.append(rescaleData2(tr_px[(i+2),(j)][color]))
            vector.append(rescaleData2(tr_px[(i),(j+1)][color]))
            vector.append(rescaleData2(tr_px[(i+1),(j+1)][color]))
            vector.append(rescaleData2(tr_px[(i+2),(j+2)][color]))
            vector.append(rescaleData2(tr_px[(i),(j+2)][color]))
            vector.append(rescaleData2(tr_px[(i+1),(j+2)][color]))
            vector.append(rescaleData2(tr_px[(i+2),(j+2)][color]))
            data.append(vector)
    
    return data

#adds model features to the dataset. Feature flag 0 denotes only quadratic features, 1 denotes quadratic and cubic features, and 2 denotes quadratic, cubic, and quartic features. 
#returns list with modified data.
def addFeatures(input_data, feature_flag):
    for i in range(len(input_data)):
        for j in range(len(input_data[i]) - 1):
            x = input_data[i][j+1]
            input_data[i].append(x ** 2)

        if(feature_flag):
            for j in range(len(input_data[i]) - 1):
                x = input_data[i][j+1]
                input_data[i].append(x ** 3)
        if(feature_flag == 2):
            for j in range(len(input_data[i]) - 1):
                x = input_data[i][j+1]
                input_data[i].append(x ** 3)
    return input_data

#given a vector of data point sub-vectors and a weight vector, calculates the dot product and then applies the 255sigmoid function to the resulting output set. 
#f(x) = 255 * sigmoid( 255 / (w0x0 + w1x1 ... + wNxN) )
#returns the weight vector. 
def applySigmoidModel(input_data, weight_vector):
    predicted_data = []
    for i in range(len(input_data)): #dot product boogaloo
        x = dotProduct(input_data[i], weight_vector)
        predicted_data.append(x)

    #sigmoid baby 
    for i in range(len(predicted_data)):
        predicted_data[i] = sigmoid(predicted_data[i])
    
    return predicted_data

#takes in a value and applies the sigmoid function to it.
#returns new value. 
def sigmoid(value):
    x = np.exp(-value)
    sig = 1. / (1 + x)
    return sig

#takes in the predicted data, and the expected data, and calculates the derivative with respect to wj for each element w in the weight vector.  
#returns the vector of derivative values
def calculateDerivatives(predicted, expected, weight_vector, input_data):
    randomDataPoint = randint(0, len(input_data))
    derivatives = []
    for i in range(len(weight_vector)):

        derivatives.append(predicted[randomDataPoint]) # sigmoid(w.x) of the random datapoint. 
        derivatives[i] = 2 * derivatives[i] # 2 * sigmoid(w.x)
        derivatives[i] = derivatives[i] - (2 * expected[randomDataPoint]) # (2 * sigmoid(w.x)) - 2y
        derivatives[i] = derivatives[i] * predicted[randomDataPoint] * (1 - predicted[randomDataPoint]) * input_data[randomDataPoint][i]
    return derivatives

#updates the weights after the derivates have been calculated and stored in a vector.
#returns updated weights.
def updateWeights(weights, derivatives):
    new_weights = [] 
    for i in range(len(weights)):
        new_weight = weights[i] - derivatives[i]
        new_weights.append(new_weight)
    
    return new_weights

#takes two vectors and applies the dot product because numpy's dogshit dot product function was fucking up my weight vector and my mental health
#returns dot product.
def dotProduct(v1, v2):
    x = 0
    for i in range(len(v1)):
        x += (v1[i] * v2[i])
    return x


def colorizeImage(reds, greens, blues, testing_img, width, height):
    
    tst_px = testing_img.load()
    colorPointer = 0
    for i in range(width-2):
        for j in range(height-2):
            tst_px[i+1,j+1] = (reds[colorPointer], greens[colorPointer], blues[colorPointer])
            colorPointer += 1
    
    testing_img.save("image_process/testing_img_COLORIZED.jpg")
    return