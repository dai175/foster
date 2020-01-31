import os
from flask import Flask, request, abort, jsonify, render_template, flash, \
    redirect, url_for
from flask_migrate import Migrate
from flask_cors import CORS

# create and configure the app
from forms import CategoryForm
from models import db, Category

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
db.app = app

migrate = Migrate(app, db)

CORS(app)


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
            description=request.form['description'],
            image=request.form['image'],
        )
        error = False

        try:
            db.session.add(category)
            db.session.commit()
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if not error:
            flash('Category ' + request.form['name'] + ' was successfully listed!')
        else:
            flash('An error occurred. Category ' + request.form['name'] + ' could not be listed.')

        categories = Category.query.order_by(Category.id).all()
        data = [category.format() for category in categories]

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
        category.image = request.form['image']
        db.session.commit()

        data = category.format()

        return redirect(url_for('get_category', category_id=category_id))

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
