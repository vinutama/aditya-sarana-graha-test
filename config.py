import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    SCRET_KEY = os.environ["DEPLOYMENT_TYPE"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig:
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        os.environ["POSTGRES_USER"],
        os.environ["POSTGRES_PASSWORD"],
        os.environ["POSTGRES_HOST"],
        "5432",
        os.environ["POSTGRES_DB"],
    )
    SQLALCHEMY_ECHO = True


class ProductionConfig:
    ENV = "production"
    DEBUG = True
