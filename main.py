from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random", methods=["GET"])
def get_random_cafe():
    all_cafes = Cafe.query.all()
    random_cafe = random.choice(all_cafes)
    print(random_cafe)
    return jsonify(name=random_cafe.name,
                   map_url=random_cafe.map_url,
                   img_url=random_cafe.img_url,
                   location=random_cafe.location,
                   seats=random_cafe.seats,
                   has_toilet=random_cafe.has_toilet,
                   has_wifi=random_cafe.has_wifi,
                   has_sockets=random_cafe.has_sockets,
                   can_take_calls=random_cafe.can_take_calls,
                   coffee_price=random_cafe.coffee_price,
                   id=random_cafe.id)

@app.route("/all", methods=["GET"])
def get_all_cafes():
    all_cafes = Cafe.query.all()
    all_cafes_list = []
    dict = {}
    for cafe in all_cafes:
        dict["name"] = cafe.name
        dict["map_url"] = cafe.map_url
        dict["img_url"] = cafe.img_url
        dict["location"] = cafe.location
        dict["seats"] = cafe.seats
        dict["has_toilet"] = cafe.has_toilet
        dict["has_wifi"] = cafe.has_wifi
        dict["has_sockets"] = cafe.has_sockets
        dict["can_take_calls"] = cafe.can_take_calls
        dict["coffee_price"] = cafe.coffee_price
        dict["id"] = cafe.id
        all_cafes_list.append(dict)
        dict = {}
    return jsonify(all_cafes_list)        

@app.route("/search", methods=["GET"])
def get_cafe_at_location():
    # This is how you get hold of the parameters given in the url, they will be given after "?" in the url.
    location = request.args.get("location")
    cafe = Cafe.query.filter_by(location=location).first()
    if cafe:
        return jsonify(name=cafe.name,
                   map_url=cafe.map_url,
                   img_url=cafe.img_url,
                   location=cafe.location,
                   seats=cafe.seats,
                   has_toilet=cafe.has_toilet,
                   has_wifi=cafe.has_wifi,
                   has_sockets=cafe.has_sockets,
                   can_take_calls=cafe.can_take_calls,
                   coffee_price=cafe.coffee_price,
                   id=cafe.id)
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})
    # At this point we actually can't test our API by typing all of the url's and the parameters. So we have something called as postman
    # in this we can test our API and we can also make the documentation.

@app.route("/add", methods=["POST"])
def add():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    try:
        db.session.commit()
        print("so happy")
    except:
        db.session.rollback()
        print("So Sad")
    return jsonify(response={"success": "Successfully added the new cafe."})
    
# PATCH request
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def patch_page(cafe_id):
    new_price = request.args.get("new_price")
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        try:
            db.session.commit()
            return jsonify(response={"success": "Successfully updated the price of the cafe."})
        except:
            db.session.rollback()
        
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})

# DELETE request
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete_page(cafe_id):
    entered_api_key = request.args.get("api_key")
    if entered_api_key == "TopSecretAPIKey":
        cafe = Cafe.query.get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            try:
                db.session.commit()
                return jsonify(response={"success": "Successfully deleted the cafe."})
            except:
                db.session.rollback()
        else:
            return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})
    else:
        return jsonify(error={"Sorry, that's not allowed. Make sure you have the correct api_key."})

## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
