import keras
import cv2
import numpy as np

def getMaxIndexList(prediction):
    maxIndex = np.argmax(prediction)
    return maxIndex


def predictionFunction(prediction):
    #get labels :
    classLabels = "beaver, dolphin, otter, seal, whale, aquarium fish, flatfish, ray, shark, trout, orchids, poppies, roses, sunflowers, tulips, bottles, bowls, cans, cups, plates, apples, mushrooms, oranges, pears, sweet peppers, clock, computer keyboard, lamp, telephone, television, bed, chair, couch, table, wardrobe, bee, beetle, butterfly, caterpillar, cockroach, bear, leopard, lion, tiger, wolf, bridge, castle, house, road, skyscraper, cloud, forest, mountain, plain, sea, camel, cattle, chimpanzee, elephant, kangaroo, fox, porcupine, possum, raccoon, skunk, crab, lobster, snail, spider, worm, baby, boy, girl, man, woman, crocodile, dinosaur, lizard, snake, turtle, hamster, mouse, rabbit, shrew, squirrel, maple, oak, palm, pine, willow, bicycle, bus, motorcycle, pickup truck, train, lawn-mower, rocket, streetcar, tank, tractor"
    LABELS = classLabels.split(", ")
    LABELS.sort()
    # print("the labels list of len :", len(LABELS))
    # print(LABELS)
    maxIndex = getMaxIndexList(prediction)
    labelPrediction = LABELS[maxIndex]
    return labelPrediction



def classifier(cropped_img_name_list,og_bounding_of_cropped_dict,model = None,api = False) :
    print("[CLASSIFICATION]")
    print("[INFO] classifier input params : ")
    print("[INFO] - cropped_img_name_list :",cropped_img_name_list)
    print("[INFO] - og_bounding_of_cropped_dict :",og_bounding_of_cropped_dict)
    #read Images-----------------------------------------------------------------------
    base_image_path = "static/images/croppedImageDirectory/"
    cropped_img_list = []
    for name in cropped_img_name_list:
        read_image = cv2.imread(base_image_path+name)
        cropped_img_list.append(read_image)
    # Image preprocessing:-------------------------------------------------------------
    classifier_input_images = []
    for im in cropped_img_list :
        #resizing
        im = cv2.resize(im,(224,224))     # resize image to match model's expected sizing
        im = im.reshape(1,224,224,3)      # return the image with shaping that TF wants.
        #scaling
        im = im/255
        classifier_input_images.append(im)
    # Classifier:
    ### Load a classifie:-------------------------------------------------------------
    if model == None :
        model = keras.models.load_model("./myModel/final_save")
    ### Classification:---------------------------------------------------------------
    prediction_list = []
    for img in classifier_input_images :
        prediction  = model.predict(img)
        prediction_list.append(prediction)


    label_list = []
    bounding_for_each_label = {}
    for i,prediction in enumerate(prediction_list):
        predicted_label = predictionFunction(prediction)
        label_list.append(predicted_label)
        if api :
            try :
                bounding_for_each_label[predicted_label].append(
                    og_bounding_of_cropped_dict[cropped_img_name_list[i]]
                )
            except :
                bounding_for_each_label[predicted_label] = []
                bounding_for_each_label[predicted_label].append(
                    og_bounding_of_cropped_dict[cropped_img_name_list[i]]
                )
    print("[INFO] label_list: ",label_list)
    print("---------------------------------------------------------------------------")
    return cropped_img_name_list,label_list,bounding_for_each_label
    #---------------------------------------------------------------------------------
