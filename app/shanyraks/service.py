from app.config import database
from pydantic import BaseSettings
from .adapters.s3_service import S3Service
from .repository.repository import ShanyrakRepository
from .adapters.here_service import HereService


class Config(BaseSettings):
    HERE_API_KEY: str


class Service:
    def __init__(
        self,
        repository: ShanyrakRepository,
    ):
        config = Config()  
        self.repository = repository
        self.s3_service = S3Service()
        self.here_service = HereService(config.HERE_API_KEY)

def get_service():
    repository = ShanyrakRepository(database)
    return Service(repository)