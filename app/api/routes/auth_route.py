from typing import Annotated
import bcrypt
from fastapi import APIRouter, Body, HTTPException, status
from app.api.errors.conflict_exception import ConflictException
from app.api.errors.email_already_exists_exception import EmailAlreadyExistsException
from app.api.models.user_model import UserRegister
from app.api.services.auth_service import (
    CommonAuthService,
)
from app.api.services.jwt_service import CommonJwtService, JwtService

router = APIRouter()


@router.post("/register")
async def register(
    user: Annotated[UserRegister, Body()],
    auth_service: CommonAuthService,
    jwt_service: CommonJwtService,
):
    # Create the user in the db if the email has not been used.
    # If it was used return the appropriate error message.
    try:
        inserted_user = await auth_service.register_user(resisted_user=user)
    except EmailAlreadyExistsException as e:
        raise ConflictException(e.message)

    # Generate a JWT token and return it.
    token = await jwt_service.generate_token(
        data={"email": inserted_user.email, "id": str(inserted_user.id)}
    )
    # Placeholder for user registration logic
    return {"token": token}


# @router.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
#         )
#     access_token = create_access_token({"sub": user["email"]})
#     return {"access_token": access_token, "token_type": "bearer"}
