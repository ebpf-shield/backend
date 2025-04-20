from pydantic import BaseModel, Field


class ExistsByIdResponseDto(BaseModel):
    """
    DTO for the response of the exists by ID check.
    """

    exists: bool = Field(
        description="Indicates whether the agent with the specified ID exists.",
    )
