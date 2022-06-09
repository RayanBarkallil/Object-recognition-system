from classifier import classifier
from detect  import detect
from TextToSpeech import getSoundOf


def getPediction(image_path):
    cropped_images_names,og_bounding_of_cropped_dict = detect(image_path)
    print(cropped_images_names)
    cropped_images_name_list,label_prediction,bounding_for_each_label = classifier(cropped_images_names,
                                                                                   og_bounding_of_cropped_dict)
    for i in range(len(label_prediction)) :
        getSoundOf(cropped_images_name_list[i].split(".")[0],label_prediction[i])
    return cropped_images_name_list,label_prediction,bounding_for_each_label
