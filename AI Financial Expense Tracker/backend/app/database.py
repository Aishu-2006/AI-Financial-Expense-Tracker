from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, IndexModel

from app.config import get_settings


settings = get_settings()
client = AsyncIOMotorClient(settings.mongodb_uri)
database: AsyncIOMotorDatabase = client[settings.mongodb_db_name]

async def ensure_indexes() -> None:
    print("Creating users indexes...")

    await database.users.create_indexes(
        [
            IndexModel([("email", ASCENDING)], unique=True, name="unique_user_email"),
            IndexModel([("role", ASCENDING)], name="user_role_lookup"),
        ]
    )

    print("Creating expenses indexes...")

    await database.expenses.create_indexes(
        [
            IndexModel([("userId", ASCENDING), ("date", ASCENDING)], name="expense_user_date"),
            IndexModel([("userId", ASCENDING), ("category", ASCENDING)], name="expense_user_category"),
        ]
    )

    print("Creating income indexes...")

    await database.income.create_indexes(
        [
            IndexModel([("userId", ASCENDING), ("date", ASCENDING)], name="income_user_date")
        ]
    )

    print("Creating goals indexes...")

    await database.goals.create_indexes(
        [
            IndexModel([("userId", ASCENDING), ("priority", ASCENDING)], name="goal_user_priority"),
            IndexModel([("userId", ASCENDING), ("goalName", ASCENDING)], name="goal_user_name"),
        ]
    )

    print("Creating debts indexes...")

    await database.debts.create_indexes(
        [
            IndexModel([("userId", ASCENDING), ("dueDate", ASCENDING)], name="debt_user_due_date"),
            IndexModel([("userId", ASCENDING), ("status", ASCENDING)], name="debt_user_status"),
        ]
    )

    print("Creating AI memory indexes...")

    await database.ai_memory.create_indexes(
        [
            IndexModel([("userId", ASCENDING), ("updatedAt", ASCENDING)], name="memory_user_updated")
        ]
    )

    print("Creating regret prediction indexes...")

    await database.regret_predictions.create_indexes(
        [
            IndexModel([("userId", ASCENDING), ("createdAt", ASCENDING)], name="regret_user_created")
        ]
    )

    print("Creating community stats indexes...")

    await database.community_stats.create_indexes(
        [
            IndexModel(
                [("city", ASCENDING), ("incomeRange", ASCENDING)],
                name="community_city_income_range",
            ),
            IndexModel([("city", ASCENDING)], name="community_city_lookup"),
        ]
    )

    print("All indexes created successfully.")

async def close_database_connection() -> None:
    client.close()


def get_database() -> AsyncIOMotorDatabase:
    return database
