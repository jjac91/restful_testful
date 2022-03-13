"""Flask app for Cupcakes"""

from flask import Flask, request, redirect, render_template, jsonify
from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }


@app.route("/api/cupcakes")
def list_all_cupcakes():
    """Return JSON {'cupcakes': [{id, flavor, size,...}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<cupcake_id>")
def list_single_dessert(cupcake_id):
    """Return JSON {'cupcake': {id, flavor, size,...}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes", methods=["POST"])
def make_new_cupcakes():
    """Create a new Cupcake obj and 
    return JSON {'cupcake': {id, flavor, size,...}}"""

    cupcake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"],
        rating=request.json["rating"],
        image=request.json["image"] or None)

    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return (jsonify(cupcake=serialized), 201)


@app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Updates a cupcake and responds w/ JSON of that update"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=serialize_cupcake(cupcake))


@app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes a particular cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")


@app.route("/")
def root():
    """returns the root page"""

    return render_template("index.html")
