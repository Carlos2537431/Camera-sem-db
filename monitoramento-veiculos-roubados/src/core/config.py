import os
try:
    # Opcional: carrega variáveis de um arquivo .env, se existir
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # Se python-dotenv não estiver instalado, apenas siga com os envs do sistema
    pass


class Settings:
    """Configurações básicas da aplicação via variáveis de ambiente.

    Fornece defaults seguros para subir localmente sem quebrar.
    """

    # App
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in {"1", "true", "yes"}

    # Database (compatível com SQLAlchemy)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data.db")

    # Integrações / Notificações
    FIREBASE_CREDENTIALS: str | None = os.getenv("FIREBASE_CREDENTIALS")
    MONUV_API_KEY: str | None = os.getenv("MONUV_API_KEY")
    DETECTA_API_KEY: str | None = os.getenv("DETECTA_API_KEY")
    ALERTA_BRASIL_API_KEY: str | None = os.getenv("ALERTA_BRASIL_API_KEY")
    NOTIFICATION_CHANNEL: str = os.getenv("NOTIFICATION_CHANNEL", "default_channel")
    # Polícia (opcional)
    POLICE_API_URL: str | None = os.getenv("POLICE_API_URL")
    POLICE_API_KEY: str | None = os.getenv("POLICE_API_KEY")


# Instância única usada pela aplicação
settings = Settings()