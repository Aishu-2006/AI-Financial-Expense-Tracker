from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database
from app.schemas import AIMemoryCreate, DebtCreate, ExpenseCreate, ExpenseUpdate, GoalCreate, IncomeCreate, RegretPredictionCreate
from app.security import get_current_user, require_admin
from app.serializers import serialize_document, serialize_user


router = APIRouter()


def user_object_id(current_user) -> ObjectId:
    return current_user["_id"]


@router.post("/expenses", status_code=status.HTTP_201_CREATED)
async def create_expense(
    payload: ExpenseCreate,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    expense = payload.model_dump()
    expense["userId"] = user_object_id(current_user)
    expense["date"] = payload.date.isoformat()
    expense["createdAt"] = datetime.now(timezone.utc)
    result = await db.expenses.insert_one(expense)
    return serialize_document(await db.expenses.find_one({"_id": result.inserted_id}))


@router.get("/expenses")
async def list_expenses(current_user=Depends(get_current_user), db: AsyncIOMotorDatabase = Depends(get_database)):
    cursor = db.expenses.find({"userId": user_object_id(current_user)}).sort("date", -1)
    return [serialize_document(expense) async for expense in cursor]


@router.patch("/expenses/{expense_id}")
async def update_expense(
    expense_id: str,
    payload: ExpenseUpdate,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    if not ObjectId.is_valid(expense_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid expense id")

    update_data = payload.model_dump(exclude_unset=True)
    if "date" in update_data:
        update_data["date"] = update_data["date"].isoformat()
    update_data["updatedAt"] = datetime.now(timezone.utc)

    result = await db.expenses.update_one(
        {"_id": ObjectId(expense_id), "userId": user_object_id(current_user)},
        {"$set": update_data},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    return serialize_document(await db.expenses.find_one({"_id": ObjectId(expense_id)}))


@router.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: str,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    if not ObjectId.is_valid(expense_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid expense id")

    result = await db.expenses.delete_one({"_id": ObjectId(expense_id), "userId": user_object_id(current_user)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")


@router.post("/income", status_code=status.HTTP_201_CREATED)
async def create_income(
    payload: IncomeCreate,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    income = payload.model_dump()
    income["userId"] = user_object_id(current_user)
    income["date"] = payload.date.isoformat()
    income["createdAt"] = datetime.now(timezone.utc)
    result = await db.income.insert_one(income)
    return serialize_document(await db.income.find_one({"_id": result.inserted_id}))


@router.post("/goals", status_code=status.HTTP_201_CREATED)
async def create_goal(
    payload: GoalCreate,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    goal = payload.model_dump()
    goal["userId"] = user_object_id(current_user)
    goal["createdAt"] = datetime.now(timezone.utc)
    result = await db.goals.insert_one(goal)
    return serialize_document(await db.goals.find_one({"_id": result.inserted_id}))


@router.post("/debts", status_code=status.HTTP_201_CREATED)
async def create_debt(
    payload: DebtCreate,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    debt = payload.model_dump()
    debt["userId"] = user_object_id(current_user)
    debt["dueDate"] = payload.dueDate.isoformat()
    debt["createdAt"] = datetime.now(timezone.utc)
    result = await db.debts.insert_one(debt)
    return serialize_document(await db.debts.find_one({"_id": result.inserted_id}))


@router.post("/ai-memory", status_code=status.HTTP_201_CREATED)
async def save_ai_memory(
    payload: AIMemoryCreate,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    memory = payload.model_dump()
    memory["userId"] = user_object_id(current_user)
    memory["updatedAt"] = datetime.now(timezone.utc)
    result = await db.ai_memory.insert_one(memory)
    return serialize_document(await db.ai_memory.find_one({"_id": result.inserted_id}))


@router.post("/regret-predictions", status_code=status.HTTP_201_CREATED)
async def save_regret_prediction(
    payload: RegretPredictionCreate,
    current_user=Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    prediction = payload.model_dump()
    prediction["userId"] = user_object_id(current_user)
    prediction["createdAt"] = datetime.now(timezone.utc)
    result = await db.regret_predictions.insert_one(prediction)
    return serialize_document(await db.regret_predictions.find_one({"_id": result.inserted_id}))


@router.get("/admin/users")
async def list_users_for_admin(admin_user=Depends(require_admin), db: AsyncIOMotorDatabase = Depends(get_database)):
    cursor = db.users.find().sort("createdAt", -1)
    return [serialize_user(user) async for user in cursor]
