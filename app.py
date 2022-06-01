from flask import Flask, render_template, request, session,redirect, url_for
from prediction import getPediction
import numpy as np
app = Flask(__name__)
app.config['SECRET_KEY'] = "superdupersecretkey"



@app.route('/',methods=['GET'])
def getIndex():
    return render_template("index.html")


@app.route("/",methods=['POST'])
def doThings():
    #save the image -----------------------------------------------------------------------------------------
    imagefile = request.files['imagefile']
    splitting = imagefile.filename.split('.')
    extension = splitting[len(splitting)-1]
    defaultFilename = "todo."+extension
    image_path ="./static/images/" + defaultFilename
    imagefile.save(image_path)

    #do prediction -----------------------------------------------------------------------------------------
    cropped_img_name_list,label_list = getPediction(image_path)

    #info dictionary for template filling ------------------------------------------------------------------
    croppedImageList_andLabels = {}
    for i in range(len(cropped_img_name_list)) :
        croppedImageList_andLabels[cropped_img_name_list[i]] = label_list[i]

    #session to pass variables to other fun ----------------------------------------------------------------
    session['croppedImageList_andLabels'] = croppedImageList_andLabels
    session['image_name'] = defaultFilename

    return redirect(url_for('showPredictions')+"?q="+label_list[0])


@app.route('/prediction',methods=['GET'])
def showPredictions():
    return render_template("prediction.html",
                           baseImage = session['image_name'],
                           croppedImageList_andLabels = session['croppedImageList_andLabels'])







if __name__ =="__main__":
    app.run(port=3000, debug=True)


