from flask import Flask, flash, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
from flask import jsonify
import os
import db as d

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/', methods=['GET'])
def face_upload_file():
    return render_template('index.html')


@app.route('/upload/done', methods=['POST'])
def face_upload():
    target = os.path.join(APP_ROOT, 'face-images/')  #folder path
    if not os.path.isdir(target):
            os.mkdir(target)     # create folder if not exits
    face_db_table = d.mongo.db.faces  # database table name
    if request.method == 'POST':
        for upload in request.files.getlist("face_image"): #multiple image handel
            filename = secure_filename(upload.filename)
            destination = "/".join([target, filename])
            upload.save(destination)
            face_db_table.insert_one({'name': filename, "destination" : destination})   #insert into database mongo db
            flash('Upload successfully Done')
        return redirect('/')

@app.route('/alldata', methods=['GET'])
def get_all_data():
  data = d.mongo.db.faces
  output = []
  for s in data.find():
    output.append({'name' : s['name'], 'destination' : s['destination']})
  return jsonify({'result' : output})

@app.route('/alldata/<name>', methods=['GET'])
def get_one_star(name):
  star = d.mongo.db.faces
  s = star.find_one({'name' : name})
  if s:
    output = {'name' : s['name'], 'destination' : s['destination']}
  else:
    output = "No such name"
  return jsonify({'result' : output})


if __name__ == '__main__':
    app.run()
