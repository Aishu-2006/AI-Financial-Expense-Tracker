from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models import DebtStatus, DebtType, ExpenseCategory, IncomeSource, UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()


class UserPublic(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: UserRole = UserRole.user
    createdAt: datetime


class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    category: ExpenseCategory
    description: str = Field(min_length=1, max_length=200)
    date: date


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(default=None, gt=0)
    category: Optional[ExpenseCategory] = None
    description: Optional[str] = Field(default=None, min_length=1, max_length=200)
    date: Optional[date] = None


class IncomeCreate(BaseModel):
    amount: float = Field(gt=0)
    source: IncomeSource
    date: date


class GoalCreate(BaseModel):
    goalName: str = Field(min_length=2, max_length=100)
    targetAmount: float = Field(gt=0)
    savedAmount: float = Field(default=0, ge=0)
    priority: int = Field(default=1, ge=1)


class DebtCreate(BaseModel):
    personName: str = Field(min_length=2, max_length=80)
    amount: float = Field(gt=0)
    interestRate: float = Field(default=0, ge=0, le=100)
    dueDate: date
    status: DebtStatus = DebtStatus.pending
    debtType: DebtType = DebtType.personal_loan


class AIMemoryCreate(BaseModel):
    goal: str = Field(min_length=2, max_length=150)
    progress: float = Field(ge=0, le=100)
    preference: Optional[str] = Field(default=None, max_length=300)
    conversationSummary: Optional[str] = Field(default=None, max_length=1000)


class RegretPredictionCreate(BaseModel):
    item: str = Field(min_length=2, max_length=120)
    price: float = Field(gt=0)
    riskScore: int = Field(ge=0, le=100)
    message: str = Field(min_length=2, max_length=500)


class CommunityStatsCreate(BaseModel):
    city: str = Field(min_length=2, max_length=80)
    incomeRange: str = Field(min_length=2, max_length=50)
    averageSavings: float = Field(ge=0)
    userSavings: float = Field(ge=0)
    percentile: float = Field(ge=0, le=100)


class FinancialStoryCreate(BaseModel):
    period: str = Field(min_length=2, max_length=50)
    totalIncome: float = Field(ge=0)
    totalExpenses: float = Field(ge=0)
    savings: float
    categoryHighlights: Optional[list[str]] = Field(default=None, max_length=10)
    goalProgressHighlights: Optional[list[str]] = Field(default=None, max_length=10)
    debtHighlights: Optional[list[str]] = Field(default=None, max_length=10)
    story: Optional[str] = Field(default=None, max_length=1500)


class GoalConflictCreate(BaseModel):
    monthlyIncome: float = Field(ge=0)
    monthlyExpenses: float = Field(ge=0)
    monthlyDebtObligations: float = Field(default=0, ge=0)
    availableSavingsRate: float = Field(ge=0)
    aiRecommendedPriority: list[str] = Field(min_length=1, max_length=20)
    userPriorityOverride: Optional[list[str]] = Field(default=None, max_length=20)
    impactSummary: Optional[str] = Field(default=None, max_length=1000)
