import os

env = os.getenv("FLASK_ENV", "development")

class Config:
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    MAIN_DATABASE_URL = os.getenv("MAIN_DATABASE_URL", "https://allenamento1a2025-default-rtdb.firebaseio.com")
    REST_API_URL = os.getenv("REST_API_URL", "https://matger-ubt-svr01.westeurope.cloudapp.azure.com")

    # JSON credentials-file based configuration:
    MAIN_DATABASE_CREDENTIALS = os.getenv("MAIN_DATABASE_CREDENTIALS", "creds/firebase-dev-keys.json")

    # Direct set-env credentials configuration (web-pages testing purposes *only*):
    MAIN_DATABASE_API_KEY =             os.getenv("MAIN_DATABASE_API_KEY", "--MISSING--")
    MAIN_DATABASE_AUTH_DOMAIN =         os.getenv("MAIN_DATABASE_AUTH_DOMAIN", "--MISSING--")
    MAIN_DATABASE_PROJECT_ID =          os.getenv("MAIN_DATABASE_PROJECT_ID", "--MISSING--")
    MAIN_DATABASE_STORAGE_BUCKET =      os.getenv("MAIN_DATABASE_STORAGE_BUCKET", "--MISSING--")
    MAIN_DATABASE_MESSAGING_SENDER_ID = os.getenv("MAIN_DATABASE_MESSAGING_SENDER_ID", "--MISSING--")
    MAIN_DATABASE_APP_ID =              os.getenv("MAIN_DATABASE_APP_ID", "--MISSING--")


class ProductionConfig(Config):
    DEBUG = False
    MAIN_DATABASE_URL = os.getenv("MAIN_DATABASE_URL", "https://piattaformariflessi-prod-default-rtdb.firebaseio.com")
    REST_API_URL = os.getenv("REST_API_URL", "https://matger-ubt-svr01.westeurope.cloudapp.azure.com")

    # JSON credentials-file based configuration:
    MAIN_DATABASE_CREDENTIALS = os.getenv("MAIN_DATABASE_CREDENTIALS", "creds/firebase-prod-keys.json")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig

}
