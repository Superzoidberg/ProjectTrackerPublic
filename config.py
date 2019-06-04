import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object): 
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' 
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') 
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://username:password@localhost/databasename' 
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mssql+pymssql://username:password@hostname/databasename'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # eMail config
    MAIL_SERVER = 'emailhostname'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    ADMINS = ['email@email.com']

    #Pagination
    PROJECTS_PER_PAGE = 50