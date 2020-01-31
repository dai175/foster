import os

from PIL import Image
from flask import Flask, request, abort, jsonify, render_template, flash, \
    redirect, url_for
from flask_migrate import Migrate
from flask_cors import CORS

# create and configure the app
import consts
from forms import CategoryForm
from models import db, Category

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
            filename = upload_image(file, category.id)
            category.image = filename
            db.session.commit()
        except:
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
        except:
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

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
