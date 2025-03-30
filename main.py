from sqlalchemy import Integer, String, Boolean, Text, ForeignKey
from flask_bootstrap import Bootstrap5
from typing import List
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///list.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class List(db.Model):
    __tablename__ = "list_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    items : Mapped[List["ListItem"]] = relationship(back_populates="list", cascade="all, delete-orphan")

class ListItem(db.Model):
    __tablename__ = "listItem_table"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item: Mapped[str] = mapped_column(String(100))
    item_due_date : Mapped[str] = mapped_column(String(100))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    list_id : Mapped[int] = mapped_column(ForeignKey("list_table.id"))
    list: Mapped["List"] = relationship(back_populates="items")


with app.app_context():
    db.create_all()

@app.route("/api/item", methods=["POST"])
def add_item_to_list():
    data = request.get_json()
    title = data.get("title")
    item_data = data.get("item")

    if not title or not item_data:
        return jsonify({"error": "Missing title or item data"}), 400

    list_obj = List.query.filter_by(name=title).first()
    if not list_obj:
        list_obj = List(name=title)
        db.session.add(list_obj)
        db.session.flush()  # Ensure list_obj.id is set

    new_item = ListItem(
        item=item_data["text"],
        item_due_date=item_data.get("due", ""),
        completed=item_data.get("completed", False),
        list_id=list_obj.id
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Item added", "id": new_item.id}), 201

@app.route("/api/item/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()
    item = ListItem.query.get_or_404(item_id)

    item.item_due_date = data.get("due", item.item_due_date)
    item.completed = data.get("completed", item.completed)

    db.session.commit()
    return jsonify({"message": "Item updated"}), 200

@app.route("/api/lists", methods=["POST"])
def create_or_update_list():
    print("getting a request to change the list")
    data = request.get_json()
    title = data.get("title")
    items_data = data.get("items", [])

    list_obj = List.query.filter_by(name=title).first()
    if not list_obj:
        list_obj = List(name=title)
        db.session.add(list_obj)
        db.session.flush() # so we can get id for the new items

    ListItem.query.filter_by(list_id=list_obj.id).delete()
    for item in items_data:
        new_item = ListItem(
            item=item["text"],
            item_due_date=item["due"],
            completed=item.get("completed", False),
            list_id=list_obj.id
        )
        db.session.add(new_item)
    db.session.commit()
    return jsonify({"message":"List saved successfully"}),201


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)


