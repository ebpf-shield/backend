from typing import Annotated

from fastapi import Depends

from app.api.models.process_model import ProcessDocument
from app.api.ui.models.dashboard_model import CommonProcessesInAgentsAggregation


class DashboardRepository:
    def __init__(self):
        pass

    async def common_processes(self):
        return await ProcessDocument.aggregate(
            [
                {"$group": {"_id": "$command", "count": {"$sum": "$count"}}},
                {"$sort": {"count": -1}},
                {"$limit": 10},
                {"$project": {"name": "$_id", "count": 1, "_id": 0}},
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
                {"$limit": 10},
            ]
        ).to_list()


def get_dashboard_repository():
    return DashboardRepository()


CommonDashboardRepository = Annotated[
    DashboardRepository, Depends(get_dashboard_repository, use_cache=True)
]
