from classifier import classifier
from detect  import detect

def getPediction(image_path):
    cropped_images_names = detect(image_path)
    cropped_images_name_list,label_prediction = classifier(cropped_images_names)
    return cropped_images_name_list,label_prediction
