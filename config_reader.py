<<<<<<< HEAD
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    payment_token: SecretStr
    diffbot_token: SecretStr
    openai_key: SecretStr
    payment_token_test: SecretStr
    support_chat_id: SecretStr
    bot_chat_id: SecretStr
    db_url: SecretStr

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

# Создаем объект конфигурации
=======
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    payment_token: SecretStr
    diffbot_token: SecretStr
    openai_key: SecretStr
    payment_token_test: SecretStr
    support_chat_id: SecretStr
    bot_chat_id: SecretStr
    db_url: SecretStr

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

# Создаем объект конфигурации
>>>>>>> 95e27f8d3faedcbdc6cdb1e790bf25e0d89a6449
config = Settings()