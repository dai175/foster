import os
from urllib.parse import urlencode

from PIL import Image
from flask import Flask, request, abort, jsonify, render_template, flash, \
    redirect, url_for, session
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import exc

import consts
from auth import requires_auth
from forms import CategoryForm, TypeForm, AnimalForm
from models import db, Category, Type, Animal


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    db.app = app

    migrate = Migrate(app, db)

    CORS(app)

    #  Resize and save image
    def upload_image(file, lead, id):
        image = Image.open(file)
        resize_image = image.resize(
            (int(image.width / image.height * consts.IMAGE_HEIGHT),
             consts.IMAGE_HEIGHT)
        )
        filename = '{}{}.png'.format(lead,
                                     str(id).zfill(consts.NUMBER_OF_DIGITS))
        mydir = os.path.dirname(__file__)
        resize_image.save(
            os.path.join(mydir + "/" + app.config['UPLOAD_FOLDER'], filename)
        )

        return filename

    @app.route('/')
    def index():
        return render_template('index.html', login=app.config['LOGIN_URI'])

    @app.route('/callback')
    def callback():
        session['logged_in'] = True
        return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        session.clear()
        params = {'returnTo': url_for('index', _external=True),
                  'client_id': app.config['CLIENT_ID']}
        return redirect('https://{}/v2/logout?{}'.
                        format(app.config['AUTH0_DOMAIN'], urlencode(params)))

    # ------------------------------------------------------------------------
    #   Categories
    # ------------------------------------------------------------------------

    @app.route('/categories')
    @requires_auth('get:categories')
    def get_categories(jwt):
        try:
            categories = Category.query.order_by(Category.id).all()
        except exc.SQLAlchemyError:
            abort(422)

        data = [category.format() for category in categories]

        return jsonify({
            'success': True,
            'form': render_template('forms/categories.html', categories=data)
        })

    @app.route('/categories/create', methods=['GET'])
    @requires_auth('create:category')
    def create_category(jwt):
        form = CategoryForm(request.form)

        return jsonify({
            'success': True,
            'form': render_template('forms/new_category.html', form=form)
        })

    @app.route('/categories/create', methods=['POST'])
    @requires_auth('create:category')
    def create_category_submission(jwt):
        form = CategoryForm()
        if not form.validate_on_submit():
            return jsonify({
                'success': False
            })

        category = Category(
            name=request.form.get('name'),
            description=request.form.get('description')
        )

        error = False

        try:
            db.session.add(category)
            db.session.commit()

            # Save images as
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

        return jsonify({
            'success': not error
        })

    @app.route('/category/<int:category_id>')
    @requires_auth('get:categories')
    def get_category(jwt, category_id):
        try:
            category = Category.query.get(category_id)
            if category is None:
                abort(404)

        except exc.SQLAlchemyError:
            abort(422)

        data = category.format()

        return jsonify({
            'success': True,
            'form': render_template('forms/category.html', category=data)
        })

    @app.route('/category/<int:category_id>/edit', methods=['GET'])
    @requires_auth('edit:category')
    def edit_category(jwt, category_id):
        form = CategoryForm(request.form)

        try:
            category = Category.query.get(category_id)
            if category is None:
                abort(404)

        except exc.SQLAlchemyError:
            abort(422)

        data = category.format()

        return jsonify({
            'success': True,
            'form': render_template(
                'forms/edit_category.html', form=form, category=data
            )
        })

    @app.route('/category/<int:category_id>/edit', methods=['PATCH'])
    @requires_auth('edit:category')
    def edit_category_submission(jwt, category_id):
        form = CategoryForm()
        if not form.validate_on_submit():
            return jsonify({
                'success': False
            })

        error = False

        try:
            category = Category.query.get(category_id)
            if category is None:
                abort(404)

            category.name = request.form['name']
            category.description = request.form['description']
            db.session.commit()

            # Save images as
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

        return jsonify({
            'success': not error
        })

    @app.route('/category/<int:category_id>/delete', methods=['DELETE'])
    @requires_auth('delete:category')
    def delete_category(jwt, category_id):
        error = False

        try:
            category = Category.query.get(category_id)
            if category is None:
                abort(404)

            category_name = category.name
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

        return jsonify({
            'success': not error
        })

    # ------------------------------------------------------------------------
    #   Types
    # ------------------------------------------------------------------------

    @app.route('/types/<int:category_id>')
    @requires_auth('get:types')
    def get_types(jwt, category_id):
        try:
            types = Type.query.filter(Type.category_id == category_id).\
                order_by(Type.id).all()
        except exc.SQLAlchemyError:
            abort(422)

        data = [type.format() for type in types]

        return jsonify({
            'success': True,
            'form': render_template('forms/types.html', types=data)
        })

    @app.route('/types/create', methods=['GET'])
    @requires_auth('create:type')
    def create_type(jwt):
        try:
            categories = Category.query.order_by(Category.id).all()
        except exc.SQLAlchemyError:
            abort(422)

        form = TypeForm(request.form)

        #  Add category list to form
        form.category.choices = [
            (category.id, category.name) for category in categories
        ]

        return jsonify({
            'success': True,
            'form': render_template('forms/new_type.html', form=form)
        })

    @app.route('/types/create', methods=['POST'])
    @requires_auth('create:type')
    def create_type_submission(jwt):
        try:
            categories = Category.query.order_by(Category.id).all()
        except exc.SQLAlchemyError:
            abort(422)

        form = TypeForm()

        #  Add category list to form
        form.category.choices = [
            (category.id, category.name) for category in categories
        ]

        if not form.validate_on_submit():
            return jsonify({
                'success': False
            })

        type = Type(
            category_id=int(request.form['category']),
            name=request.form['name'],
            description=request.form['description']
        )

        error = False

        try:
            db.session.add(type)
            db.session.commit()

            # Save images as
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

        return jsonify({
            'success': not error
        })

    @app.route('/type/<int:type_id>')
    @requires_auth('get:types')
    def get_type(jwt, type_id):
        try:
            type = Type.query.get(type_id)
            if type is None:
                abort(404)

            category = Category.query.get(type.category_id)
            if category is None:
                abort(404)

        except exc.SQLAlchemyError:
            abort(422)

        data = type.format()
        data['category'] = category

        return jsonify({
            'success': True,
            'form': render_template('forms/type.html', type=data)
        })

    @app.route('/type/<int:type_id>/edit', methods=['GET'])
    @requires_auth('edit:type')
    def edit_type(jwt, type_id):
        try:
            categories = Category.query.order_by(Category.id).all()

            type = Type.query.get(type_id)
            if type is None:
                abort(404)

        except exc.SQLAlchemyError:
            abort(422)

        data = type.format()

        form = TypeForm(request.form)

        #  Add category list to form
        form.category.choices = [
            (category.id, category.name) for category in categories
        ]
        form.category.default = type.category_id
        form.process()

        return jsonify({
            'success': True,
            'form': render_template(
                'forms/edit_type.html', form=form, type=data
            )
        })

    @app.route('/type/<int:type_id>/edit', methods=['PATCH'])
    @requires_auth('edit:type')
    def edit_type_submission(jwt, type_id):
        try:
            categories = Category.query.order_by(Category.id).all()
        except exc.SQLAlchemyError:
            abort(422)

        form = TypeForm()

        #  Add category list to form
        form.category.choices = [
            (category.id, category.name) for category in categories
        ]

        if not form.validate_on_submit():
            return jsonify({
                'success': False
            })

        error = False

        try:
            type = Type.query.get(type_id)
            if type is None:
                abort(404)

            type.name = request.form['name']
            type.description = request.form['description']
            type.category_id = int(request.form['category'])
            db.session.commit()

            # Save images as
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

        return jsonify({
            'success': not error
        })

    @app.route('/type/<int:type_id>/delete', methods=['DELETE'])
    @requires_auth('delete:type')
    def delete_type(jwt, type_id):
        error = False

        try:
            type = Type.query.get(type_id)
            if type is None:
                abort(404)

            type_name = type.name
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

        return jsonify({
            'success': not error
        })

    # ------------------------------------------------------------------------
    #   Animals
    # ------------------------------------------------------------------------

    @app.route('/animals/<int:type_id>')
    @requires_auth('get:animals')
    def get_animals(jwt, type_id):
        try:
            animals = Animal.query.filter(Animal.type_id == type_id).\
                order_by(Animal.id).all()
        except exc.SQLAlchemyError:
            abort(422)

        data = [animal.format() for animal in animals]

        return jsonify({
            'success': True,
            'form': render_template('forms/animals.html', animals=data)
        })

    @app.route('/animals/create', methods=['GET'])
    @requires_auth('create:animal')
    def create_animal(jwt):
        try:
            types = Type.query.order_by(Type.id).all()
        except exc.SQLAlchemyError:
            abort(422)

        form = AnimalForm(request.form)

        #  Add category list to form
        form.type.choices = [
            (type.id, type.name) for type in types
        ]

        return jsonify({
            'success': True,
            'form': render_template('forms/new_animal.html', form=form)
        })

    @app.route('/animals/create', methods=['POST'])
    @requires_auth('create:animal')
    def create_animal_submission(jwt):
        try:
            types = Type.query.order_by(Type.id).all()
        except exc.SQLAlchemyError:
            abort(422)

        form = AnimalForm()

        #  Add category list to form
        form.type.choices = [
            (type.id, type.name) for type in types
        ]
        if not form.validate_on_submit():
            return jsonify({
                'success': False
            })

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

            # Save images as
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

        return jsonify({
            'success': not error
        })

    @app.route('/animal/<int:animal_id>')
    @requires_auth('get:animals')
    def get_animal(jwt, animal_id):
        try:
            animal = Animal.query.get(animal_id)
            if animal is None:
                abort(404)

            type = Type.query.get(animal.type_id)
            if type is None:
                abort(404)

        except exc.SQLAlchemyError:
            abort(422)

        data = animal.format()
        data['type'] = type

        return jsonify({
            'success': True,
            'form': render_template('forms/animal.html', animal=data)
        })

    @app.route('/animal/<int:animal_id>/edit', methods=['GET'])
    @requires_auth('edit:animal')
    def edit_animal(jwt, animal_id):
        try:
            types = Type.query.order_by(Type.id).all()

            animal = Animal.query.get(animal_id)
            if animal is None:
                abort(404)

        except exc.SQLAlchemyError:
            abort(422)

        data = animal.format()

        form = AnimalForm(request.form)

        #  Add category list to form
        form.type.choices = [
            (type.id, type.name) for type in types
        ]
        form.type.default = animal.type_id
        form.process()

        return jsonify({
            'success': True,
            'form': render_template(
                'forms/edit_animal.html', form=form, animal=data
            )
        })

    @app.route('/animal/<int:animal_id>/edit', methods=['PATCH'])
    @requires_auth('edit:animal')
    def edit_animal_submission(jwt, animal_id):
        try:
            types = Type.query.order_by(Type.id).all()
        except exc.SQLAlchemyError:
            abort(422)

        form = AnimalForm()

        #  Add category list to form
        form.type.choices = [
            (type.id, type.name) for type in types
        ]
        if not form.validate_on_submit():
            return jsonify({
                'success': False
            })

        error = False

        try:
            animal = Animal.query.get(animal_id)
            if animal is None:
                abort(404)

            animal.name = request.form['name']
            animal.sex = request.form['sex']
            animal.date_of_birth = request.form['date_of_birth']
            animal.weight = request.form['weight']
            animal.place_of_birth = request.form['place_of_birth']
            animal.description = request.form['description']
            animal.type_id = int(request.form['type'])
            db.session.commit()

            # Save images as
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

        return jsonify({
            'success': not error
        })

    @app.route('/animal/<int:animal_id>/delete', methods=['DELETE'])
    @requires_auth('delete:animal')
    def delete_animal(jwt, animal_id):
        error = False

        try:
            animal = Animal.query.get(animal_id)
            if animal is None:
                abort(404)

            animal_name = animal.name
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

        return jsonify({
            'success': not error
        })

    # ------------------------------------------------------------------------
    #   Error handler
    # ------------------------------------------------------------------------

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
