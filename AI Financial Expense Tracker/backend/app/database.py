from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, IndexModel

from app.config import get_settings


settings = get_settings()
client = AsyncIOMotorClient(settings.mongodb_uri)
database: AsyncIOMotorDatabase = client[settings.mongodb_db_name]


async def ensure_indexes() -> None:
    await database.users.create_indexes(
        [
            IndexModel([("email", ASCENDING)], unique=True, name="unique_user_email"),
            IndexModel([("role", ASCENDING)], name="user_role_lookup"),
        ]
    )
    await database.expenses.create_indexes(
        [
            IndexModel([("userId", ASCENDING), ("date", ASCENDING)], name="expense_user_date"),
            IndexModel([("userId", ASCENDING), ("category", ASCENDING)], name="expense_user_category"),
        ]
    )
    await database.income.create_indexes(
        [IndexModel([("userId", ASCENDING), ("date", ASCENDING)], name="income_user_date")]
    )
    await database.goals.create_indexes(
        [
            IndexModel([("userId", ASCENDING), ("priority", ASCENDING)], name="goal_user_priority"),
            IndexModel([("userId", ASCENDING), ("goalName", ASCENDING)], name="goal_user_name"),
        ]
    )
    await database.debts.create_indexes(
        [
            IndexModel([("userId", ASCENDING), ("dueDate", ASCENDING)], name="debt_user_due_date"),
            IndexModel([("userId", ASCENDING), ("status", ASCENDING)], name="debt_user_status"),
        ]
    )
    await database.ai_memory.create_indexes(
        [IndexModel([("userId", ASCENDING), ("updatedAt", ASCENDING)], name="memory_user_updated")]
    )
    await database.regret_predictions.create_indexes(
        [IndexModel([("userId", ASCENDING), ("createdAt", ASCENDING)], name="regret_user_created")]
    )


async def close_database_connection() -> None:
    client.close()


def get_database() -> AsyncIOMotorDatabase:
    return database
