from typing import Annotated

from fastapi import Depends


class HostProcessService:
    pass


def get_process_service():
    return HostProcessService()


CommonHostProcessService = Annotated[
    HostProcessService, Depends(get_process_service, use_cache=True)
]
