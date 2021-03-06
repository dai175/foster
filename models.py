from flask_sqlalchemy import SQLAlchemy

database_name = "foster"
database_path = "postgres://{}/{}".\
    format('user:password@localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    image = db.Column(db.String)
    types = db.relationship('Type', backref='category', lazy=True)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image
        }


class Type(db.Model):
    __tablename__ = 'type'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    image = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    animals = db.relationship('Animal', backref='type', lazy=True)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
        }


class Animal(db.Model):
    __tablename__ = 'animal'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    sex = db.Column(db.Integer)
    date_of_birth = db.Column(db.Date)
    weight = db.Column(db.Float)
    place_of_birth = db.Column(db.String)
    description = db.Column(db.String)
    image = db.Column(db.String)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)

    def format(self):
        sex_dict = {1: 'male', 2: 'female'}
        return {
            'id': self.id,
            'name': self.name,
            'sex': sex_dict[self.sex],
            'date_of_birth': self.date_of_birth,
            'weight': self.weight,
            'place_of_birth': self.place_of_birth,
            'description': self.description,
            'image': self.image
        }
