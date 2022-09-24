import os
from flask import Flask , render_template , request
import model as m 

UPLOAD_FOLDER = "./images"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/' ,methods=['GET'])
def hello_world():
    #if request.method == 'GET':
    #   print('get')
    return render_template('main.html')
    #return 'Hello, World!'

@app.route('/',methods=['POST'])
def predict():
    imagefile= request.files['imagefile']
    img_path = os.path.join(app.config["UPLOAD_FOLDER"],imagefile.filename)
    imagefile.save(img_path)
    image_cnv=m.image_convert(img_path)
    imo=image_cnv
    return render_template('index.html') 

if __name__ == "__main__":
   app.run(debug=True)