import os
import secrets
from turtle import title
from datetime import timedelta, date
from PIL import Image #converting the image to smaller pixels
from flask import Flask, render_template, url_for, flash, redirect, request
from flasklrc import app, db, bcrypt, mail
from flasklrc.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                            AddBooksForm, Check_in, Check_out, RequestResetForm, 
                            ResetPasswordForm, ChangePasswordForm)
from flasklrc.models import Students, Books, New_data, Old_data
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/")
@app.route("/home")
def home():
    posts = Books.query.all()
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Students(gnumber=form.gnumber.data, name=form.name.data, email=form.email.data, 
                            password=hashed_password)
        db.session.add(student)
        db.session.commit()
        flash('Your Account is now created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title = 'Register', form = form)

    
@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Students.query.filter_by(gnumber=form.gnumber.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccesful. Please check Gnumber and Password!', 'danger')
    return render_template('login.html',title = 'Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # reducing the size of the image  
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.gnumber = form.gnumber.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.gnumber.data = current_user.gnumber
        form.email.data = current_user.email
        form.name.data = current_user.name
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', 
                            image_file=image_file, form=form)


@app.route("/add_books", methods=['GET','POST'])
@login_required
def add_books():
    if current_user.gnumber == 'G60426042':
        form = AddBooksForm()
        if form.validate_on_submit():
            book = Books(ISBN=form.ISBN.data, publisher=form.publisher.data, name=form.name.data, 
                        author=form.author.data, level=form.level.data)
            db.session.add(book)
            db.session.commit()
            flash('Book has been added successfully!!', 'success')
            return redirect(url_for('home'))
        return render_template('add_books.html', title='ADD Books', form=form)


@app.route("/check_in", methods=['GET','POST'])
@login_required
def check_in():
    if current_user.gnumber == 'G60426042':
        form = Check_in()
        if form.validate_on_submit():
            d_checked = date.today()
            d_returned = d_checked + timedelta(days=21)
            new_data = New_data( gnumber = form.gnumber.data, ISBN = form.ISBN.data ,
                                date_issued = d_checked, date_returned = d_returned)
            db.session.add(new_data)
            db.session.commit()
            flash('Entry added successfully', 'success')
            return redirect(url_for('check_in'))
        return render_template('check_in.html', title='Check In Books', form = form)


@app.route("/not_returned")
@login_required
def not_returned():
    if current_user.gnumber == 'G60426042':
        posts = New_data.query.all()
        return render_template('not_returned.html', title='Books not returned', posts=posts, Students=Students, Books=Books)


@app.route("/check_out", methods=['GET','POST'])
@login_required
def check_out():
    if current_user.gnumber == 'G60426042':
        form = Check_out()
        if form.validate_on_submit():
            New_data.query.filter_by(gnumber=form.gnumber.data,
                                                ISBN = form.ISBN.data).delete()
            old_data = Old_data(gnumber = form.gnumber.data, ISBN = form.ISBN.data)
            db.session.add(old_data)
            db.session.commit()
            flash('Entry added successfully', 'success')
            return redirect(url_for('check_out'))
        return render_template('check_out.html', title='Check Out Books', form = form)


@app.route("/history")
@login_required
def history():
    if current_user.gnumber == 'G60426042':
        posts = Old_data.query.all()
        return render_template('history.html', title='Books returned', posts=posts)


def send_reset_email(stud):
    token = stud.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[stud.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
   

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        stud = Students.query.filter_by(email=form.email.data).first()
        send_reset_email(stud)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

    
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    stud = Students.verify_reset_token(token)
    if stud is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        stud.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/data/<gnumber>", methods=['GET', 'POST'])
@login_required
def stud_data(gnumber):
    if current_user.gnumber == 'G60426042':
        stud = Students.query.filter_by(gnumber=gnumber).first()
        check_ins = New_data.query.filter_by(gnumber=gnumber)
        check_outs = Old_data.query.filter_by(gnumber=gnumber)
        return render_template('stud_data.html', gnumber=stud.gnumber,
                                name=stud.name, email=stud.email ,check_ins=check_ins, 
                                check_outs=check_outs)


@app.route("/book/<ISBN>", methods=['GET', 'POST'])
@login_required
def book_data(ISBN):
    if current_user.gnumber == 'G60426042':
        book1 = Books.query.filter_by(ISBN=ISBN).first()
        return render_template('book_data.html', book1=book1)

