from flask import Flask, redirect, url_for, flash, request, render_template
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# initializing app.
app = Flask(__name__)
app.config['SECRET_KEY'] = '791628bb0b13ce0c676dfd7'

# initializing database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# DATABSE MODEL
class TODO(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(200), nullable= False)
    date_created = db.Column(db.DateTime(), default= datetime.now)
    
# FORM MODELS
class AddForm(FlaskForm):
    add_field = StringField('Add Field', validators= [DataRequired()])
    add_btn = SubmitField('Add Task')

class UpdateForm(FlaskForm):
    update_field = StringField('Update Field', validators= [DataRequired()])
    update_btn = SubmitField('Update')

@app.route('/', methods = ['POST', 'GET'])
@app.route('/index', methods= ["POST", "GET"])
def index():
    form = AddForm()
    if request.method == "POST":
        add_content = form.add_field.data
        new_task = TODO(text= add_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            flash('Task has been successfully added!', 'success')
            return redirect('/')
        except:
            flash("Something went wrong while adding task to database.", 'danger')

    else:
        all_tasks = TODO.query.order_by(TODO.date_created).all()
        return render_template('index.html', form= form, tasks = all_tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = TODO.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash('Task completed!', 'success')
        return redirect('/')
    except:
        flash("Something went wrong while removing task.", 'danger')


@app.route('/update/<int:id>', methods= ["POST", "GET"])
def update(id):
    form = UpdateForm()
    task_to_update = TODO.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.text = request.form['update_field']
        try:
            db.session.commit()
            flash('Task has been updated!', 'success')
            return redirect('/')
        except:
            flash("Something went wrong while updating the task.", 'danger')

    else:
        return render_template('update.html', task= task_to_update, form= form)


if __name__ == '__main__':
    app.run(debug= True)
