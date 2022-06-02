from classifier import classifier
from detect  import detect
from TextToSpeech import getSoundOf


def getPediction(image_path):
    cropped_images_names = detect(image_path)
    cropped_images_name_list,label_prediction = classifier(cropped_images_names)
    for i in range(len(label_prediction)) :
        getSoundOf(cropped_images_name_list[i].split(".")[0],label_prediction[i])
    return cropped_images_name_list,label_prediction
