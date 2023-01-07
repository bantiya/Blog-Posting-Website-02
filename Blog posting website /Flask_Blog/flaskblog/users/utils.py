import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail



def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # used to create a random name of 8 bits
    _, f_ext = os.path.splitext(form_picture.filename) # it splits the filename of the picture that the user uploaded to filenmae and extension
    picture_fn = random_hex + f_ext # making a new filename with random_hex and the extension
    # we need to get a full path to which the profile is going to save so we use os path
    # it join with app.route_path joined with static/profile_pics and joined with the picture_fn name
    picture_path = os.path.join(current_app.root_path,'static/profile_pics',picture_fn)
    # from the pillow package in order to resize the profile pic to a thumbnail
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


# sending token to the email
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)