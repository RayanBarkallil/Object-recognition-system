from flask import Flask, render_template, request, session,redirect, url_for,jsonify
from flask_restful import Api, Resource
from prediction import getPediction


app = Flask(__name__)
app.config['SECRET_KEY'] = "superdupersecretkey"
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/',methods=['GET'])
def getIndex():
    return render_template("index.html")


@app.route("/",methods=['POST'])
def doThings():
    #save the image -----------------------------------------------------------------------------------------
    imagefile = request.files['imagefile']
    splitting = imagefile.filename.split('.')
    extension = splitting[len(splitting)-1].lower()
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



#API SECTION :
#test--------------------------------------------------------------------------------------------------
api = Api(app)
todos ={}
class ObjectDetectionAPI(Resource):
    def post(self):
        imagefile = request.files['imagefile']
        splitting = imagefile.filename.split('.')
        extension = splitting[len(splitting)-1].lower()
        defaultFilename = "todo."+extension
        image_path ="./static/images/" + defaultFilename
        imagefile.save(image_path)
        #do prediction -----------------------------------------------------------------------------------------
        cropped_img_name_list,label_list = getPediction(image_path)
        #info dictionary for template filling ------------------------------------------------------------------
        croppedImageList_andLabels = {}
        for i in range(len(cropped_img_name_list)) :
            croppedImageList_andLabels[cropped_img_name_list[i]] = {
                "label" : label_list[i] #todo add coordinates 3la kulla rectangle
            }
        return croppedImageList_andLabels


api.add_resource(ObjectDetectionAPI, "/api/detect")


if __name__=="__main__":
    app.run(host= '0.0.0.0',port=5000,debug=True)