import cv2
from math import sqrt,pow
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def distanceFrom(self,point):
        X = self.x-point.x
        Y = self.y-point.y
        return sqrt(pow(X,2)+pow(Y,2))


def eleminateRedondantRect(listOfRectangles,tolerancePixel,w_tolerance,h_tolerance):
    resultList = [listOfRectangles[0]]
    for (ex,ey,ew,eh) in listOfRectangles[1:] :
        centerOfMass = Point((ex+ew)/2,(ey+eh)/2)
        centerOfMassCondition = True
        for (tmp_ex,tmp_ey,tmp_ew,tmp_eh) in resultList:
            #compare center of gravity
            tmp_centerOfMass = Point((tmp_ex+tmp_ew)/2,(tmp_ey+tmp_eh)/2)
            if centerOfMass.distanceFrom(tmp_centerOfMass) > tolerancePixel :
                continue
            else :
                #check width & height
                if ew-tmp_ew > w_tolerance or eh-tmp_eh > h_tolerance :
                    resultList.append((ex,ey,ew,eh))
                    break
                else :
                    centerOfMassCondition = False
                    continue
        if centerOfMassCondition == True :
            resultList.append((ex,ey,ew,eh))
    print(resultList)
    return resultList




def detect(image_path):
    #charger l'image et la redimentionner
    img_og = cv2.imread(image_path)
    H,W = img_og.shape[0],img_og.shape[1]
    #scaling :
    new_w = 1000
    scale = float(new_w/W)
    new_h = int(H*scale)
    img = cv2.resize(img_og, (new_w,new_h),interpolation = cv2.INTER_AREA)
    # haar code :
    #get superlabels :
    SUPER_LABELS = ["aquatic mammals","fish","flowers","food containers","household electrical devices","fruit and vegetables","household furniture","large carnivores","insects","large man-made outdoor things","large natural outdoor scenes","medium-sized mammals","large omnivores and herbivores","non-insect invertebrates","reptiles","people","trees","small mammals","vehicles"]
    SUPER_LABELS.sort()

    #dictionnaire detecters :
    cascade_dic = {}
    for superclass in SUPER_LABELS :
        cascade_dic[superclass] = cv2.CascadeClassifier('haar/haar_cascades/'+superclass+'_cascade.xml')
    #RQ : le nom du detecteur doit obligatoirement suivre la nomeclature : superclass+'_cascade.xml'

    #sauvegarder les coordonnées du rectangle:
    #make it grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #---------------------------------get rectangle coordinates--------------------------
    haar_list_outputs = []
    for superLabel in SUPER_LABELS :
        try :
            rectangle_list = cascade_dic[superLabel].detectMultiScale(
                                    image=gray,
                                    scaleFactor=1.1, 
                                    minNeighbors=50, 
                                    minSize=(400,400),
                                    maxSize=(1000,1000)
                                )
            haar_list_outputs.append(rectangle_list)
        except:
            continue
    #-------------------------------------------------------------------------------------

    #on élemine la superposition des rectangles
    #----------------------------- eleminate redondant rect -------------------------------
    #create big list fiha kulchi les rectangles
    big_list_of_rectangles = []
    for cascade_output in haar_list_outputs :
        for (ex,ey,ew,eh) in cascade_output:
            big_list_of_rectangles.append((ex,ey,ew,eh))

    #elemination process
    tolerance_pixel_value = 150
    w_tolerance = 50
    h_tolerance = 50
    final_rectangle_list = eleminateRedondantRect(big_list_of_rectangles,
                                                  tolerance_pixel_value,
                                                  w_tolerance,
                                                  h_tolerance)
    #todo NMS
    #-------------------------------------------------------------------------------------


    #on coupe l'image selon le rectangle:
    #--------------------------------- cropping the images -------------------------------
    print("[INFO] final_rectangle_list after elemination process: ",final_rectangle_list)
    base_image_path = "static/images/croppedImageDirectory/"
    image_name_index = 1
    og_bounding_of_cropped_dict = {}
    cropped_image_name_list = []
    for (ex,ey,ew,eh) in final_rectangle_list :
        #cropping
        cropped_img = img[ey:ey+eh,ex:ex+ew]
        #bounding boxes rescale to OG
        rescaled_x = int(ex/scale)
        rescaled_y = int(ey/scale)
        rescaled_w = int(ew/scale)
        rescaled_h = int(eh/scale)
        rescaled_to_OG_detection_dimension = (rescaled_x,rescaled_y,rescaled_w,rescaled_h)
        print("[INFO] rescaled_to_OG_detection_dimension : ",rescaled_to_OG_detection_dimension)
        #save the cropped image
        image_name = str(image_name_index)+".jpg"
        image_path = base_image_path+image_name
        cv2.imwrite(image_path,cropped_img)
        cropped_image_name_list.append(image_name)
        image_name_index += 1
        #save to dic :
        og_bounding_of_cropped_dict[image_name] = rescaled_to_OG_detection_dimension

        # cropped_img_list.append(cropped_img)
    print("[INFO] cropped_image_name_list : ",cropped_image_name_list)
    print("[INFO] og_bounding_of_cropped_dict : ",og_bounding_of_cropped_dict)
    #-------------------------------------------------------------------------------------
    return cropped_image_name_list,og_bounding_of_cropped_dict