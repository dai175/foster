import os

from PIL import Image
from flask import Flask, request, abort, jsonify, render_template, flash, \
    redirect, url_for
from flask_migrate import Migrate
from flask_cors import CORS

# create and configure the app
from sqlalchemy import exc

import consts
from forms import CategoryForm, TypeForm
from models import db, Category, Type

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
db.app = app

migrate = Migrate(app, db)

CORS(app)


def upload_image(file, id):
    image = Image.open(file)
    resize_image = image.resize(
        (int(image.width / image.height * consts.IMAGE_HEIGHT),
         consts.IMAGE_HEIGHT)
    )
    filename = 'c{}.png'.format(str(id).zfill(consts.NUMBER_OF_DIGITS))
    resize_image.save(
        os.path.join(app.config['UPLOAD_FOLDER'], filename)
    )

    return filename


def create_app(test_config=None):
    @app.route('/')
    def index():
        return render_template('index.html')

    # ------------------------------------------------------------------------
    #   Categories
    # ------------------------------------------------------------------------

    @app.route('/categories')
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
                filename = upload_image(file, category.id)
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

    @app.route('/category/<int:category_id>/edit', methods=['POST'])
    def edit_category_submission(category_id):
        category = Category.query.get(category_id)
        category.name = request.form['name']
        category.description = request.form['description']

        error = False

        try:
            db.session.commit()

            file = request.files['image']
            if file:
                filename = upload_image(file, category_id)
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
                filename = upload_image(file, type.id)
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

    @app.route('/type/<int:type_id>/edit', methods=['POST'])
    def edit_type_submission(type_id):
        type = Type.query.get(type_id)
        type.name = request.form['name']
        type.description = request.form['description']
        type.category_id = int(request.form['category'])

        error = False

        try:
            db.session.commit()

            file = request.files['image']
            if file:
                filename = upload_image(file, type_id)
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

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
