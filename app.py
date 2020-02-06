import json
import os

from PIL import Image
from flask import Flask, request, abort, jsonify, render_template, flash, \
    redirect, url_for
from flask_migrate import Migrate
from flask_cors import CORS

# create and configure the app
from sqlalchemy import exc

import consts
from auth import requires_auth
from forms import CategoryForm, TypeForm, AnimalForm
from models import db, Category, Type, Animal

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
db.app = app

migrate = Migrate(app, db)

CORS(app)


# ------------------------------------------------------------------------
#   General functions
# ------------------------------------------------------------------------

def upload_image(file, lead, id):
    image = Image.open(file)
    resize_image = image.resize(
        (int(image.width / image.height * consts.IMAGE_HEIGHT),
         consts.IMAGE_HEIGHT)
    )
    filename = '{}{}.png'.format(lead, str(id).zfill(consts.NUMBER_OF_DIGITS))
    resize_image.save(
        os.path.join(app.config['UPLOAD_FOLDER'], filename)
    )

    return filename


# ------------------------------------------------------------------------
#   Main
# ------------------------------------------------------------------------

def create_app(test_config=None):
    @app.route('/')
    def index():
        return render_template('index.html',
                               login=app.config['LOGIN_URI']
                               )

    @app.route('/callback')
    def callback():
        return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    # ------------------------------------------------------------------------
    #   Categories
    # ------------------------------------------------------------------------

    @app.route('/categories')
    @requires_auth()
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        data = [category.format() for category in categories]

        return render_template('categories.html', categories=data)

    @app.route('/categories/create', methods=['GET'])
    def create_category():
        form = CategoryForm(request.form)

        return render_template('new_category.html', form=form)

    @app.route('/categories/create', methods=['POST'])
    def create_category_submission():
        category = Category(
            name=request.form['name'],
            description=request.form['description']
        )

        error = False

        try:
            db.session.add(category)
            db.session.commit()

            file = request.files['image']
            if file:
                filename = upload_image(
                    file, consts.LEAD_CATEGORY, category.id
                )
                category.image = filename
                db.session.commit()
        except exc.SQLAlchemyError:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if not error:
            flash('Category {} was successfully listed!'.
                  format(request.form['name']))
        else:
            flash('An error occurred. Category {} could not be listed.'.
                  format(request.form['name']))

        return redirect(url_for('get_categories'))

    @app.route('/category/<int:category_id>')
    def get_category(category_id):
        category = Category.query.get(category_id)
        data = category.format()

        return render_template('category.html', category=data)

    @app.route('/category/<int:category_id>/edit', methods=['GET'])
    def edit_category(category_id):
        form = CategoryForm(request.form)

        category = Category.query.get(category_id)
        data = category.format()

        return render_template('edit_category.html', form=form, category=data)

    @app.route('/category/<int:category_id>/edit', methods=['POST', 'PATCH'])
    def edit_category_submission(category_id):
        # if request.method != 'PATCH' and \
        #         request.form.get('_method') != 'PATCH':
        #     pass

        category = Category.query.get(category_id)
        category.name = request.form['name']
        category.description = request.form['description']

        error = False

        try:
            db.session.commit()

            file = request.files['image']
            if file:
                filename = upload_image(
                    file, consts.LEAD_CATEGORY, category_id
                )
                category.image = filename
                db.session.commit()
        except exc.SQLAlchemyError:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if not error:
            flash('Category {} was successfully updated!'.
                  format(request.form['name']))
        else:
            flash('An error occurred. Category {} could not be updated.'.
                  format(request.form['name']))

        return redirect(url_for('get_category', category_id=category_id))

    @app.route('/category/<int:category_id>/delete',
               methods=['POST', 'DELETE'])
    def delete_category(category_id):
        # if request.method != 'DELETE' and \
        #         request.form.get('_method') != 'DELETE':
        #     pass

        category = Category.query.get(category_id)
        category_name = category.name
        error = False

        try:
            db.session.delete(category)
            db.session.commit()
        except exc.SQLAlchemyError:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if not error:
            flash('Category {} was successfully deleted!'.
                  format(category_name))
        else:
            flash('An error occurred. Category {} could not be deleted.'.
                  format(category_name))

        return redirect(url_for('get_categories'))

    # ------------------------------------------------------------------------
    #   Types
    # ------------------------------------------------------------------------

    @app.route('/types')
    def get_types():
        data = []
        categories = Category.query.order_by(Category.id).all()
        for category in categories:
            types = Type.query.filter(Type.category_id == category.id).all()
            formatted_types = [type.format() for type in types]
            item = category.format()
            item['types'] = formatted_types
            data.append(item)

        return render_template('types.html', categories=data)

    @app.route('/types/create', methods=['GET'])
    def create_type():
        categories = Category.query.order_by(Category.id).all()

        form = TypeForm(request.form)
        form.category.choices = [
            (category.id, category.name) for category in categories
        ]

        return render_template('new_type.html', form=form)

    @app.route('/types/create', methods=['POST'])
    def create_type_submission():
        type = Type(
            category_id=int(request.form['category']),
            name=request.form['name'],
            description=request.form['description']
        )

        error = False

        try:
            db.session.add(type)
            db.session.commit()

            file = request.files['image']
            if file:
                filename = upload_image(file, consts.LEAD_TYPE, type.id)
                type.image = filename
                db.session.commit()
        except exc.SQLAlchemyError:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if not error:
            flash('Type {} was successfully listed!'.
                  format(request.form['name']))
        else:
            flash('An error occurred. Type {} could not be listed.'.
                  format(request.form['name']))

        return redirect(url_for('get_types'))

    @app.route('/type/<int:type_id>')
    def get_type(type_id):
        type = Type.query.get(type_id)
        data = type.format()
        data['category'] = Category.query.get(type.category_id)

        return render_template('type.html', type=data)

    @app.route('/type/<int:type_id>/edit', methods=['GET'])
    def edit_type(type_id):
        categories = Category.query.order_by(Category.id).all()
        type = Type.query.get(type_id)
        data = type.format()

        form = TypeForm(request.form)
        form.category.choices = [
            (category.id, category.name) for category in categories
        ]
        form.category.default = type.category_id
        form.process()

        return render_template('edit_type.html', form=form, type=data)

    @app.route('/type/<int:type_id>/edit', methods=['POST', 'PATCH'])
    def edit_type_submission(type_id):
        # if request.method != 'PATCH' and \
        #         request.form.get('_method') != 'PATCH':
        #     pass

        type = Type.query.get(type_id)
        type.name = request.form['name']
        type.description = request.form['description']
        type.category_id = int(request.form['category'])

        error = False

        try:
            db.session.commit()

            file = request.files['image']
            if file:
                filename = upload_image(file, consts.LEAD_TYPE, type_id)
                type.image = filename
                db.session.commit()
        except exc.SQLAlchemyError:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if not error:
            flash('Type {} was successfully updated!'.
                  format(request.form['name']))
        else:
            flash('An error occurred. Type {} could not be updated.'.
                  format(request.form['name']))

        return redirect(url_for('get_type', type_id=type_id))

    @app.route('/type/<int:type_id>/delete',
               methods=['POST', 'DELETE'])
    def delete_type(type_id):
        # if request.method != 'DELETE' and \
        #         request.form.get('_method') != 'DELETE':
        #     pass

        type = Type.query.get(type_id)
        type_name = type.name

        error = False

        try:
            db.session.delete(type)
            db.session.commit()
        except exc.SQLAlchemyError:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if not error:
            flash('Type {} was successfully deleted!'.
                  format(type_name))
        else:
            flash('An error occurred. Type {} could not be deleted.'.
                  format(type_name))

        return redirect(url_for('get_types'))

    # ------------------------------------------------------------------------
    #   Animals
    # ------------------------------------------------------------------------

    @app.route('/animals')
    def get_animals():
        data = []
        types = Type.query.order_by(Type.id).all()
        for type in types:
            animals = Animal.query.filter(Animal.type_id == type.id).all()
            formatted_animals = [animal.format() for animal in animals]
            item = type.format()
            item['animals'] = formatted_animals
            data.append(item)

        return render_template('animals.html', types=data)

    @app.route('/animals/create', methods=['GET'])
    def create_animal():
        types = Type.query.order_by(Type.id).all()

        form = AnimalForm(request.form)
        form.type.choices = [
            (type.id, type.name) for type in types
        ]

        return render_template('new_animal.html', form=form)

    @app.route('/animals/create', methods=['POST'])
    def create_animal_submission():
        # form = AnimalForm(request.form)
        # if not form.validate():
        #     return render_template('new_animal.html', form=form)

        animal = Animal(
            type_id=int(request.form['type']),
            name=request.form['name'],
            sex=int(request.form['sex']),
            date_of_birth=request.form['date_of_birth'],
            weight=request.form['weight'],
            place_of_birth=request.form['place_of_birth'],
            description=request.form['description']
        )

        error = False

        try:
            db.session.add(animal)
            db.session.commit()

            file = request.files['image']
            if file:
                filename = upload_image(file, consts.LEAD_ANIMAL, animal.id)
                animal.image = filename
                db.session.commit()
        except exc.SQLAlchemyError:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if not error:
            flash('Animal {} was successfully listed!'.
                  format(request.form['name']))
        else:
            flash('An error occurred. Animal {} could not be listed.'.
                  format(request.form['name']))

        return redirect(url_for('get_animals'))

    @app.route('/animal/<int:animal_id>')
    def get_animal(animal_id):
        animal = Animal.query.get(animal_id)
        data = animal.format()
        data['type'] = Type.query.get(animal.type_id)

        return render_template('animal.html', animal=data)

    @app.route('/animal/<int:animal_id>/edit', methods=['GET'])
    def edit_animal(animal_id):
        types = Type.query.order_by(Type.id).all()
        animal = Animal.query.get(animal_id)
        data = animal.format()

        form = AnimalForm(request.form)
        form.type.choices = [
            (type.id, type.name) for type in types
        ]
        form.type.default = animal.type_id
        form.sex.default = animal.sex
        form.process()

        return render_template('edit_animal.html', form=form, animal=data)

    @app.route('/animal/<int:animal_id>/edit', methods=['POST', 'PATCH'])
    def edit_animal_submission(animal_id):
        # if request.method != 'PATCH' and \
        #         request.form.get('_method') != 'PATCH':
        #     pass

        animal = Animal.query.get(animal_id)
        animal.name = request.form['name']
        animal.sex = request.form['sex']
        animal.date_of_birth = request.form['date_of_birth']
        animal.weight = request.form['weight']
        animal.place_of_birth = request.form['place_of_birth']
        animal.description = request.form['description']
        animal.type_id = int(request.form['type'])

        error = False

        try:
            db.session.commit()

            file = request.files['image']
            if file:
                filename = upload_image(file, consts.LEAD_ANIMAL, animal_id)
                animal.image = filename
                db.session.commit()
        except exc.SQLAlchemyError:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if not error:
            flash('Animal {} was successfully updated!'.
                  format(request.form['name']))
        else:
            flash('An error occurred. Animal {} could not be updated.'.
                  format(request.form['name']))

        return redirect(url_for('get_animal', animal_id=animal_id))

    @app.route('/animal/<int:animal_id>/delete',
               methods=['POST', 'DELETE'])
    def delete_animal(animal_id):
        # if request.method != 'DELETE' and \
        #         request.form.get('_method') != 'DELETE':
        #     pass

        animal = Animal.query.get(animal_id)
        animal_name = animal.name

        error = False

        try:
            db.session.delete(animal)
            db.session.commit()
        except exc.SQLAlchemyError:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if not error:
            flash('Animal {} was successfully deleted!'.
                  format(animal_name))
        else:
            flash('An error occurred. Animal {} could not be deleted.'.
                  format(animal_name))

        return redirect(url_for('get_animals'))

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
