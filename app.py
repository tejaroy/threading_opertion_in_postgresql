from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:205101tejaT@localhost:5432/teja'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate=Migrate(app,db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    sample_id = db.Column(db.String(10))
    state = db.Column(db.String(100))
    nation = db.Column(db.String(10))
    date_of_test=db.Column(db.String(100))
    date_of_sample=db.Column(db.String(100))
    age=db.Column(db.String(100))
    postive_negitive=db.Column(db.String(100))
    present_residence=db.Column(db.String(100))
    phonenumber=db.Column(db.String(100))
    address=db.Column(db.String(100))
    collection_date=db.Column(db.String(100))
    village=db.Column(db.String(100))

    def __repr__(self):
        return f"id:{self.id},name:{self.name},sample_id:{self.sample_id},state:{self.state},nation:{self.nation},date_of_test:{self.date_of_test},date_of_sample:{self.date_of_sample},age:{self.age},postive_negitive:{self.postive_negitive},present_residence:{self.present_residence},phonenumber:{self.phonenumber},address:{self.address},collection_date:{self.collection_date},village:{self.village}"


@app.route('/user', methods=['GET'])
def user():
    users = User.query.all()
    output=[]
    for data in users:
        output.append({
            'id':data.id,
            'name':data.name,
            'sample_id':data.sample_id,
            'state' :data.state,
            'nation' :data.nation,
            'date_of_test':data.date_of_test,
            'date_of_sample':data.date_of_sample,
            'age':data.age,
            'postive_negitive':data.postive_negitive,
            'present_residence':data.present_residence,
            'phonenumber':data.phonenumber,
            'address':data.address,
            'collection_date':data.collection_date,
            'village':data.village
        })
    print(users)
    return jsonify({"code": 200, "message": "users data fetch successfully",'users': output})

@app.route('/user/<int:id>',methods=['GET'])
def get(id):
    user = User.query.filter_by(id=id)
    output = []
    for data in user:
        output.append({
            'id': data.id,
            'name': data.name,
            'sample_id': data.sample_id,
            'state': data.state,
            'nation': data.nation,
            'date_of_test': data.date_of_test,
            'date_of_sample': data.date_of_sample,
            'age': data.age,
            'postive_negitive': data.postive_negitive,
            'present_residence': data.present_residence,
            'phonenumber': data.phonenumber,
            'address': data.address,
            'collection_date': data.collection_date,
            'village': data.village
        })
    if user:
        return {"code": 200, "message": "user data fetch successfully", 'user': output}
    return {"code": 404, 'message': 'user not found'}


@app.route('/add', methods=['POST'])
def signup():
    data = request.form
    name=data.get('name')
    sample_id=data.get('sample_id')
    state=data.get("state")
    date_of_test=data.get("date_of_test")
    date_of_sample=data.get('date_of_sample')
    nation=data.get('nation')
    age=data.get('age')
    postive_negitive=data.get('postive_negitive')
    present_residence=data.get('present_residence')
    phonenumber=data.get('phonenumber')
    address=data.get('address')
    collection_date=data.get('collection_date')
    village=data.get('village')

    user = User.query.filter_by(sample_id=sample_id).first()
    if not user:
        user = User(
            name=name,
            sample_id=sample_id,
            state=state,
            nation=nation,
            date_of_test=date_of_test,
            date_of_sample=date_of_sample,
            age=age,
            address=address,
            postive_negitive=postive_negitive,
            present_residence=present_residence,
            phonenumber=phonenumber,
            collection_date=collection_date,
            village=village
        )
        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered.', 201)
    else:
        return make_response('User already exists   ', 202)

@app.route('/user/<int:id>',methods=['PUT'])
def put(id):
    data = request.form
    user = User.query.filter_by(id=id).first()
    if user:
        user.name = data["name"]
        user.sample_id = data["sample_id"]
        user.state = data["state"]
        user.nation = data["nation"]
        user.date_of_test=data["date_of_test"]
        user.date_of_sample=data["date_of_sample"]
        user.age=data["age"]
        user.address=data["address"]
        user.postive_negitive=data["postive_negitive"]
        user.present_residence=data["present_residence"]
        user.phonenumber=data["phonenumber"]
        user.collection_date=data["collection_date"]
        user.village=data["village"]
    else:
        user = User(id=id, **data)
    db.session.add(user)
    db.session.commit()
    return {"code": 200, "message": "user data update successfully", 'user':data}


@app.route('/user/<int:id>',methods=['DELETE'])
def delete(id):
    user =User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return {"code": 204, "message": "user data delete successfully"}
    else:
        return {"code": 404, "message": "user not found"}


if __name__=='__main__':
    app.run(debug=True)