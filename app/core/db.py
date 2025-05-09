import logging
from typing import Annotated
from beanie import init_beanie
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.models.agent_model import AgentDocument
from app.api.models.process_model import ProcessDocument
from app.api.models.rule_model import RuleDocument
from app.api.ui.models.user_model import UserDocument
from app.core.config import settings


logger = logging.getLogger(__name__)


class MongoDBClientManager:
    _client: AsyncIOMotorClient | None = None

    @property
    def mongo_client(self) -> AsyncIOMotorClient:
        return self._client

    async def start_async_mongo(self):
        try:
            self._client = AsyncIOMotorClient(settings.CONNECTION_STRING)
            await init_beanie(
                self._client[settings.DB_NAME],
                document_models=[
                    UserDocument,
                    RuleDocument,
                    AgentDocument,
                    ProcessDocument,
                    RuleDocument,
                ],
            )
            logger.info("Connected to mongoDB")

        except Exception as _e:
            print(_e)
            logger.error("Unable to connect to mongoDB")
            print("Error")

    async def close_mongo(self):
        if self._client is None:
            raise Exception("MongoDB client is not initialized.")

        try:
            self._client.close()
            logger.info("Closed connection to MongoDB")
        except Exception as _e:
            logger.error("Unable to close connection to MongoDB")
            raise _e

    async def get_session(self):
        if self._client is None:
            raise Exception("MongoDB client is not initialized.")

        return await self._client.start_session()

    def get_mongo_client(self) -> AsyncIOMotorClient:
        return self.mongo_client


mongo_client_manager = MongoDBClientManager()
CommonMongoClient = Annotated[
    AsyncIOMotorClient, Depends(mongo_client_manager.get_mongo_client, use_cache=True)
]
