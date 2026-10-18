from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://ain:change_me@localhost:5432/ain"
    kafka_bootstrap: str = "localhost:29092"
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_user: str = "bridge"
    mqtt_password: str = ""
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = ""
    minio_secret_key: str = ""
    minio_secure: bool = False

    jwt_secret: str = "dev-only-change-me"
    jwt_expire_min: int = 30

    vision_weights: str = "models/vision/weights/best.pt"
    vision_min_conf: float = 0.5

    # Fusion (قابلة للتعديل علشان الـ ablation)
    fusion_enabled: bool = True
    fusion_radius_m: float = 50
    fusion_window_min: float = 30
    fusion_threshold: float = 0.5
    fusion_w_space: float = 0.5
    fusion_w_time: float = 0.3
    fusion_w_source: float = 0.2

    # Priority weights
    prio_w_type: float = 0.4
    prio_w_geo: float = 0.25
    prio_w_sources: float = 0.2
    prio_w_conf: float = 0.15


settings = Settings()
