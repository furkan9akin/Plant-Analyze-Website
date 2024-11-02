from flask import Flask, render_template, request, redirect, flash
import os
import tarim
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

UPLOAD_FOLDER = 'static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

@app.route("/")
def anasayfa():
    return render_template("index.html")

@app.route("/home")
def anasayfa2():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100), nullable=False)

    mesaj = db.Column(db.String(200), nullable=False)

    # Nesnenin ve kimliğin çıktısı
    def __repr__(self):
        return f'<Card {self.id}>'

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method == "POST":
       fullname = request.form.get("fullname")
       mesaj = request.form.get("mesaj")
       if fullname != "" and mesaj != "":
        card = Card(fullname=fullname, mesaj=mesaj)
            
        db.session.add(card)
        db.session.commit()

        flash("Mesajı gönderdiniz!","success")
       else:
        flash("İsim ve mesaj bilgilerini doldurunuz.","error")
       return redirect('/contact')
    else:   
        return render_template('contact.html')

# Dosya yükleme işlemi
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Dosya yolunu oluştur
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        # Dosyayı kaydet
        file.save(file_path)
        x = tarim.kerass(file_path)
        a = ["Tomato: ","Strawberry: ","Potato: ","Corn: ","Grape: ","Peach: ","Cherry: ","Bell pepper: ","Apple: "]
        # Yüklenen dosyanın URL'ini frontend'e gönder
        labeled_values = list(zip(a, x))
        return render_template('index.html', filename=file.filename,labeled_values=labeled_values)



if __name__ == "__main__":
    with app.app_context():
         db.create_all()
    app.run(debug=True)