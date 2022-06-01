import cv2

def eleminateRedondantRect(listOfRectangles):
    #todo eleminate redondant rectangles
    return None




def detect(image_path):
    #charger l'image et la redemisentionner
    img = cv2.imread(image_path)
    img = cv2.resize(img, (1000,1000),interpolation = cv2.INTER_AREA)
    # haar code :
    #get labels :
    classLabels = "beaver, dolphin, otter, seal, whale, aquarium fish, flatfish, ray, shark, trout, orchids, poppies, roses, sunflowers, tulips, containers	bottles, bowls, cans, cups, plates, apples, mushrooms, oranges, pears, sweet peppers, clock, computer keyboard, lamp, telephone, television, bed, chair, couch, table, wardrobe, bee, beetle, butterfly, caterpillar, cockroach, bear, leopard, lion, tiger, wolf, bridge, castle, house, road, skyscraper, cloud, forest, mountain, plain, sea, camel, cattle, chimpanzee, elephant, kangaroo, fox, porcupine, possum, raccoon, skunk, crab, lobster, snail, spider, worm, baby, boy, girl, man, woman, crocodile, dinosaur, lizard, snake, turtle, hamster, mouse, rabbit, shrew, squirrel, maple, oak, palm, pine, willow, bicycle, bus, motorcycle, pickup truck, train, lawn-mower, rocket, streetcar, tank, tractor"
    LABELS = classLabels.split(", ")
    LABELS.sort()

    #get superlabels :
    SUPER_LABELS = ["aquatic mammals","fish","flowers","food containers","household electrical devices","fruit and vegetables","household furniture","large carnivores","insects","large man-made outdoor things","large natural outdoor scenes","medium-sized mammals","large omnivores and herbivores","non-insect invertebrates","reptiles","people","trees","small mammals","vehicles"]
    SUPER_LABELS.sort()

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
    final_rectangle_list = eleminateRedondantRect(big_list_of_rectangles)
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

    #on les sauvegarde dans le images/croppedImageDirectory
    #------------------------------- saving cropped images -------------------------------
    image_name_list = []
    image_index = 1
    base_image_path = "static/images/croppedImageDirectory/"
    for img in cropped_img_list :
        image_name = str(image_index)+".jpg"
        image_path = base_image_path+image_name
        cv2.imwrite(image_path,img)
        image_name_list.append(image_name)
        image_index +=1
    #-------------------------------------------------------------------------------------
    print(image_name_list)
    return image_name_list