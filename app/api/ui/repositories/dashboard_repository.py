from typing import Annotated

from fastapi import Depends

from app.api.models.agent_model import AgentDocument
from app.api.models.process_model import ProcessDocument
from app.api.models.rule_model import RuleDocument
from app.api.ui.models.dashboard_model import (
    AgentLocationProjection,
    AgentsByIsOnlineAggregation,
    CommonProcessesInAgentsAggregation,
    ProcessesStatusCount,
    RulesByChainAggregation,
)
from app.api.ui.models.user_model import UserDocument


class DashboardRepository:
    def __init__(self):
        pass

    async def common_processes(self):
        return await ProcessDocument.aggregate(
            [
                {"$group": {"_id": "$command", "count": {"$sum": "$count"}}},
                {"$project": {"name": "$_id", "count": 1, "_id": 0}},
                {"$sort": {"count": -1}},
                {"$limit": 10},
            ],
            CommonProcessesInAgentsAggregation,
        ).to_list()

    async def processes_with_most_rules(self):
        return await ProcessDocument.aggregate(
            [
                {
                    "$lookup": {
                        "from": "rules",
                        "localField": "_id",
                        "foreignField": "processId",
                        "as": "rules",
                    }
                },
                {"$addFields": {"rulesCount": {"$size": "$rules"}}},
                {"$match": {"rulesCount": {"$gt": 0}}},
                {"$group": {"_id": "$command", "rulesCount": {"$sum": "$rulesCount"}}},
                {"$project": {"name": "$_id", "rulesCount": 1, "_id": 0}},
                {"$sort": {"rulesCount": -1}},
                {"$limit": 10},
            ]
        ).to_list()

    async def rules_by_chain(self):
        return await RuleDocument.aggregate(
            [
                {"$group": {"_id": "$chain", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ],
            RulesByChainAggregation,
        ).to_list()

    async def agent_locations(self):
        """
        Returns a list of all agent external IPs.
        """
        return (
            await AgentDocument.find(
                {"geolocationProperties": {"$exists": True}},
            )
            .project(AgentLocationProjection)
            .to_list()
        )

    async def processes_by_status(self):
        return await ProcessDocument.aggregate(
            [
                {
                    "$group": {
                        "_id": "$status",
                        "count": {"$sum": 1},
                    }
                },
                {
                    "$project": {
                        "status": "$_id",
                        "count": 1,
                        "_id": 0,
                    }
                },
            ],
            ProcessesStatusCount,
        ).to_list()

    async def agents_by_is_online(self):
        return await AgentDocument.aggregate(
            [
                {
                    "$addFields": {
                        "status": {
                            "$cond": {
                                "if": "$online",
                                "then": "online",
                                "else": "offline",
                            }
                        }
                    }
                },
                {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            ],
            AgentsByIsOnlineAggregation,
        ).to_list()

    async def users_by_is_active(self):
        """
        Returns a list of users with their active status.
        """
        return await UserDocument.count()


def get_dashboard_repository():
    return DashboardRepository()


CommonDashboardRepository = Annotated[
    DashboardRepository, Depends(get_dashboard_repository, use_cache=True)
]
