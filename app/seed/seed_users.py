from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import async_session
from app.models.user import User, Role
from app.config.security import get_password_hash  # adjust import if needed
import asyncio

# Sample users and roles
roles_data = ["admin", "manager", "staff"]

users_data = [
    {
        "username": "admin_user",
        "email": "admin@example.com",
        "password": "adminpass",
        "role": "admin"
    },
    {
        "username": "manager_user",
        "email": "manager@example.com",
        "password": "managerpass",
        "role": "manager"
    },
    {
        "username": "staff_user",
        "email": "staff@example.com",
        "password": "staffpass",
        "role": "staff"
    }
]

async def seed_users():
    async with async_session() as session:
        # Create roles
        role_objs = {}
        for role_name in roles_data:
            role = Role(name=role_name)
            session.add(role)
            await session.flush()
            role_objs[role_name] = role

        # Create users
        for user_data in users_data:
            hashed_pw = get_password_hash(user_data["password"])
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=hashed_pw,
                role=role_objs[user_data["role"]]
            )
            session.add(user)

        await session.commit()
        print("Users and roles seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_users())
