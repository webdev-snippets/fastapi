from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str = "sqlite:///database.db"
    debug_level: str = "DEBUG"
    expire_time: str = "30"
    issuer: str = "test-api"

    model_config = SettingsConfigDict(env_file=".env")


SCOPES: dict = {
    "user": "allow read access to user",
    "user:write": "allow r/w access to user",
    "user:delete": "allow delete access to a user",
    "booking": "allow read access to users bookings",
    "booking:write": "allow r/w accessz to user bookings",
    "booking:delete": "allow delete4 acess to user bookings"
}
