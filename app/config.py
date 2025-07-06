from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    metrics_collection_interval: float = 5.0  #after every 5seconds collect system metrics
    histogram_buckets: list = [0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0]

settings = Settings() #instance of the Settings class. To use singleton pattern.