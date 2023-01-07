import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') #secret cookie so that the user can
                                                              #stay logged in even after he has closed the browser
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') #the '///' are a relative path from current file
    # for sending emails
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True 
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')