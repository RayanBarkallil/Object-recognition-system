from flask import Flask, render_template, request
from prediction import getPediction

app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello_world():
    return render_template("index.html")

@app.route("/",methods=['POST'])
def doThings():
    imagefile = request.files['imagefile']
    image_path ="./images/" + imagefile.filename
    imagefile.save(image_path)
    label_list = getPediction(image_path)
    return label_list





if __name__ =="__main__":
    app.run(port=3000, debug=True)


