from uuid import uuid4
from loguru import logger
from backend.app.core.db import driver
from backend.app.core.security import create_access_token, get_password_hash, verify_password
from backend.app.schemas.user import UserCreate

class AuthDAO:
    def register(self, request: UserCreate) -> dict:
        encrypted_password = get_password_hash(request.password)

        try:
            # First check if user exists
            records, _, _ = driver.execute_query(
                """
                MATCH (u:User {email: $email}) 
                RETURN u
                """,
                email=request.email
            )
            
            if records:
                logger.error(f"User with email {request.email} already exists")
                return {"error": "User with this email already exists"}

            # If no user exists, create new one
            records, _, _ = driver.execute_query(
                """
                CREATE (u:User {
                    email: $email,
                    name: $name,
                    password: $password,
                    id: $id
                })
                RETURN u
                """,
                email=request.email,
                name=request.name,
                password=encrypted_password,
                id=str(uuid4())
            )
            logger.debug(f"Successfully registered user with email {request.email}")
            return records[0]['u']

        except Exception as e:
            logger.error(f"Error registering user: {str(e)}")
            return {"error": str(e)}
    
    """
    This method should attempt to find a user by the email address provided
    and attempt to verify the password.

    If a user is not found or the passwords do not match, a `false` value should
    be returned.  Otherwise, the users properties should be returned along with
    an encoded JWT token with a set of 'claims'.

    {
      userId: 'some-random-uuid',
      email: 'graphacademy@neo4j.com',
      name: 'GraphAcademy User',
      token: '...'
    }
    """
    def authenticate(self, email: str, plain_password: str) -> dict:
        try:
            records, summary, keys = driver.execute_query(
                """
                MATCH (u:User {email: $email}) RETURN u
                """,
                email=email,
            )
            if records:
                user = records[0]["u"]
                if not verify_password(plain_password, user["password"]):
                    return {"error": "Invalid email or password"}
                token = create_access_token({"sub": user["id"]})
                return {"token": token}
            else:
                return {"error": "Invalid email or password"}
        except Exception as e:
            return {"error": str(e)}

authdao = AuthDAO()