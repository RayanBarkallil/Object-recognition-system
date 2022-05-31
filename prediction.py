import classifier
import detect 

def pediction(image_path):
    cropped_images = detect.detect(image_path)
    label_prediction = classifier.classifier(cropped_images)
    return label_prediction
