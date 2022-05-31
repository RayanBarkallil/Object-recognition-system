import cv2
from cv2 import dnn
from flask import request
from keras.preprocessing.image import load_img
import matplotlib.pyplot as plt
import keras


import numpy as np

def detect():


    #charger l'image et la redemisentionner
    img = load_img(image_path,target_size=(1000,1000))

    # haar code :
    #get labels :
    classLabels = "beaver, dolphin, otter, seal, whale, aquarium fish, flatfish, ray, shark, trout, orchids, poppies, roses, sunflowers, tulips, containers	bottles, bowls, cans, cups, plates, apples, mushrooms, oranges, pears, sweet peppers, clock, computer keyboard, lamp, telephone, television, bed, chair, couch, table, wardrobe, bee, beetle, butterfly, caterpillar, cockroach, bear, leopard, lion, tiger, wolf, bridge, castle, house, road, skyscraper, cloud, forest, mountain, plain, sea, camel, cattle, chimpanzee, elephant, kangaroo, fox, porcupine, possum, raccoon, skunk, crab, lobster, snail, spider, worm, baby, boy, girl, man, woman, crocodile, dinosaur, lizard, snake, turtle, hamster, mouse, rabbit, shrew, squirrel, maple, oak, palm, pine, willow, bicycle, bus, motorcycle, pickup truck, train, lawn-mower, rocket, streetcar, tank, tractor"
    LABELS = classLabels.split(", ")
    LABELS.sort()
    print("the labels list of len :", len(LABELS))
    print(LABELS)
    #get superlabels :
    SUPER_LABELS = ["aquatic mammals","fish","flowers","food containers","household electrical devices","fruit and vegetables","household furniture","large carnivores","insects","large man-made outdoor things","large natural outdoor scenes","medium-sized mammals","large omnivores and herbivores","non-insect invertebrates","reptiles","people","trees","small mammals","vehicles"]
    SUPER_LABELS.sort()
    print("superclass_list len = ",len(SUPER_LABELS))
    print(SUPER_LABELS)
    #dictionnaire detecters :
    cascade_dic = {}
    cropped_img_list = []
    for superclass in SUPER_LABELS :
        cascade_dic[superclass] = cv2.CascadeClassifier('haar/haar_cascades/'+superclass+'_cascade.xml')
    #RQ : le nom du detecteur doit obligatoirement suivre la nomeclature : superclass+'_cascade.xml'

    #sauvegarder les coordonnées du rectangle:
    #make it grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #---------------------------------get rectangle coordinates--------------------------
    haar_list_outputs = []
    for superLabel in SUPER_LABELS :
        print(superLabel)
        try :
            rectangle_list = cascade_dic[superLabel].detectMultiScale(
                                    image=gray, 
                                    scaleFactor=1.1, 
                                    minNeighbors=50, 
                                    minSize=(500,500),
                                    maxSize=(1000,1000)
                                )
            haar_list_outputs.append(rectangle_list)
        except:
            continue
    print(haar_list_outputs)
    #-------------------------------------------------------------------------------------

    #on coupe l'image selon le rectangle:
    #--------------------------------- cropping the images -------------------------------
    for cascade_output in haar_list_outputs :
        for (ex,ey,ew,eh) in cascade_output:
            #draw renctangles
    #         cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),5)   
            #cropping
            cropped_img = img[ey:ey+eh,ex:ex+ew]
            cropped_img_list.append(cropped_img)
    #-------------------------------------------------------------------------------------
    return cropped_img_list