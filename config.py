class Config:
    SECRET_KEY = "super-secret-key"
    JWT_SECRET_KEY = "super-secret-key"

    # REQUIRED FOR SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = "sqlite:///mechanics.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
