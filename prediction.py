from classifier import classifier
from detect  import detect
import os

def getPediction(image_path,model,api = False):
    cropped_images_names,og_bounding_of_cropped_dict = detect(image_path)
    print(cropped_images_names)
    cropped_images_name_list,label_prediction,bounding_for_each_label = classifier(cropped_images_names,
                                                                                   og_bounding_of_cropped_dict,
                                                                                   model,
                                                                                   api)

    # for i in range(len(label_prediction)) :
        # print("get sound of : ",label_prediction[i])
        # getSoundOf(cropped_images_name_list[i].split(".")[0],label_prediction[i])

    return cropped_images_name_list,label_prediction,bounding_for_each_label
