import keras
import cv2
import numpy as np

def getMaxIndexList(prediction):
    maxIndex = np.argmax(prediction)
    return maxIndex


def predictionFunction(prediction):
    #get labels :
    classLabels = "beaver, dolphin, otter, seal, whale, aquarium fish, flatfish, ray, shark, trout, orchids, poppies, roses, sunflowers, tulips, containers	bottles, bowls, cans, cups, plates, apples, mushrooms, oranges, pears, sweet peppers, clock, computer keyboard, lamp, telephone, television, bed, chair, couch, table, wardrobe, bee, beetle, butterfly, caterpillar, cockroach, bear, leopard, lion, tiger, wolf, bridge, castle, house, road, skyscraper, cloud, forest, mountain, plain, sea, camel, cattle, chimpanzee, elephant, kangaroo, fox, porcupine, possum, raccoon, skunk, crab, lobster, snail, spider, worm, baby, boy, girl, man, woman, crocodile, dinosaur, lizard, snake, turtle, hamster, mouse, rabbit, shrew, squirrel, maple, oak, palm, pine, willow, bicycle, bus, motorcycle, pickup truck, train, lawn-mower, rocket, streetcar, tank, tractor"
    LABELS = classLabels.split(", ")
    LABELS.sort()
    print("the labels list of len :", len(LABELS))
    print(LABELS)
    maxIndex = getMaxIndexList(prediction)
    labelPrediction = LABELS[maxIndex]
    return labelPrediction



def classifier(cropped_img_list) :
    # Image preprocessing:
    classifier_input_images = []
    for im in cropped_img_list :
        #resizing
        im = cv2.resize(im,(224,224))     # resize image to match model's expected sizing
        im = im.reshape(1,224,224,3)      # return the image with shaping that TF wants.
        #scaling
        im = im/255
        classifier_input_images.append(im)
    len(classifier_input_images)
    # Classifier:
    ### Load a classifie:
    model = keras.models.load_model("./myModel/final_save")
    # model.summary()
    ### Classification:
    prediction_list = []
    for img in classifier_input_images :
        prediction  = model.predict(img)
        prediction_list.append(prediction)
    label_list = []
    for prediction in prediction_list:
        predicted_label = predictionFunction(prediction)
        label_list.append(predicted_label)
    print(label_list)
    return label_list

