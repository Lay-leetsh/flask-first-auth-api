class Config:
    # Flask 404 Help off
    ERROR_404_HELP = False

    # jwt
    SECRET_KEY = 'my_secret_key'
    JWT_SECRET_KEY = 'my_jwt_secret_key'

    # mysql
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = 'password'
    MYSQL_DATABASE_DB = 'lay'
    MYSQL_DATABASE_HOST = 'localhost'

    # SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db}'.format(
        user=MYSQL_DATABASE_USER,
        password=MYSQL_DATABASE_PASSWORD,
        host=MYSQL_DATABASE_HOST,
        db=MYSQL_DATABASE_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
