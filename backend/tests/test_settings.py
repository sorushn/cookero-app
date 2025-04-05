from backend.app.settings import settings
import configparser


def test_settings():
    config = configparser.ConfigParser()
    config.read("..//settings.ini")
    assert settings.get("database", "DB_USER") == config.get("database", "DB_USER")
    assert settings.get("database", "DB_PASSWORD") == config.get(
        "database", "DB_PASSWORD"
    )
    assert settings.get("database", "DB_PORT") == config.get("database", "DB_PORT")
