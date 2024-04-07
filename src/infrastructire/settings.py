import functools
import importlib.metadata

import dotenv
import pydantic
import pydantic_settings

dotenv.load_dotenv()


class Db(pydantic_settings.BaseSettings, case_sensitive=True):
    """Database config"""

    HOSTNAME: str
    PORT: int
    DATABASE: str

    USER: str
    PASSWORD: str

    @property
    def dsn(self) -> pydantic.MySQLDsn:
        return pydantic.MySQLDsn(
            f"mysql+asyncmy://{self.USER}:{self.PASSWORD}@{self.HOSTNAME}:{self.PORT}/{self.DATABASE}",
        )

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="MYSQL_")


class Redis(pydantic_settings.BaseSettings, case_sensitive=True):
    """Redis config"""

    HOSTNAME: str
    PORT: int
    DATABASE: int
    USER: str
    PASSWORD: str

    @property
    def dsn(self) -> pydantic.RedisDsn:
        return pydantic.RedisDsn(f"redis://{self.HOSTNAME}:{self.PORT}/")

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="REDIS_")


class Amqp(pydantic_settings.BaseSettings, case_sensitive=True):
    HOSTNAME: str
    USER: str
    PASSWORD: str

    @property
    def dsn(self) -> pydantic.AmqpDsn:
        return pydantic.AmqpDsn(f"amqp://{self.USER}:{self.PASSWORD}@{self.HOSTNAME}")

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="AMQP_")


class Logging(pydantic_settings.BaseSettings, case_sensitive=True):
    """Logging config"""

    LEVEL: str = pydantic.Field(default="DEBUG")
    COLORIZE: bool = pydantic.Field(default=True)
    SERIALIZE: bool = pydantic.Field(default=False)

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="LOGGING_")


@functools.lru_cache
def get_amqp_url() -> str:
    return str(Amqp().dsn)


@functools.lru_cache
def get_mysql_url() -> str:
    return str(Db().dsn)


@functools.lru_cache
def get_redis_url() -> str:
    return str(Redis().dsn)


app_name = "scada-api"
version = importlib.metadata.version(app_name)
logging_settings = Logging()
