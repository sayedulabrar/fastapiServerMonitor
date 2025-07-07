from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    metrics_collection_interval: float = 5.0  #after every 5seconds collect system metrics
    histogram_buckets: list = [0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0]
    BYTES_BUCKETS = [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000]

settings = Settings() #instance of the Settings class. To use singleton pattern.