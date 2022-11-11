from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Guide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(100), unique=True)
    pword1 = db.Column(db.String(100), unique=False)
    pword2 = db.Column(db.String(100), unique=False)
    addr1 = db.Column(db.String(100), unique=False)
    addr2 = db.Column(db.String(100), unique=False)
    city = db.Column(db.String(100), unique=False)
    state = db.Column(db.String(2), unique=False)
    zipcode = db.Column(db.String(5), unique=False)
    phone = db.Column(db.String(10), unique=False)
    saved = db.Column(db.String(3), unique=False)
    sdate = db.Column(db.String(10), unique=False)
    bdate = db.Column(db.String(10), unique=False)

    def __init__(self, fname, email, pword1, pword2, addr1, addr2, city, state, zipcode, phone, saved, sdate, bdate):
        self.fname = fname
        self.email = email
        self.pword1 = pword1
        self.pword2 = pword2
        self.addr1 = addr1
        self.addr2 = addr2
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.phone = phone
        self.saved = saved
        self.sdate = sdate
        self.bdate = bdate


class GuideSchema(ma.Schema):
    class Meta:

        fields = ('fname',  'email', 'pword1', 'pword2', 'addr1', 'addr2', 'city',
                  'state', 'zipcode', 'phone', 'saved', 'sdate', 'bdate')


guide_schema = GuideSchema()
guides_schema = GuideSchema(many=True)


@ app.route("/guide", methods=["POST"])
def add_note():
    fname = request.json['fname']
    email = request.json['email']
    pword1 = request.json['pword1']
    pword2 = request.json['pword2']
    addr1 = request.json['addr1']
    addr2 = request.json['addr2']
    city = request.json['city']
    state = request.json['mystate']
    zipcode = request.json['zipcode']
    phone = request.json['phone']
    saved = request.json['saved']
    sdate = request.json['sdate']
    bdate = request.json['bdate']

    new_guide = Guide(fname, email, pword1, pword2, addr1, addr2,
                      city, state, zipcode, phone, saved, sdate, bdate)

    db.session.add(new_guide)
    db.session.commit()

    return guide_schema.jsonify(new_guide), 201


@ app.route("/login", methods=["POST"])
def login_user():
    email = request.json['email']
    pword1 = request.json['pword1']

    user = Guide.query.filter(Guide.email == email).first()

    if pword1 == user.pword1:
        return jsonify({'success': True, 'user': guide_schema.dump(user)}), 200
    else:
        return jsonify({'success': False}), 403


@ app.route("/guide", methods=["GET"])
def get_guide():
    all_guide = Guide.query.all()
    result = guide_schema.dump(all_guide)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
