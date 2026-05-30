from enum import Enum


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class ExpenseCategory(str, Enum):
    food = "Food"
    travel = "Travel"
    shopping = "Shopping"
    bills = "Bills"
    entertainment = "Entertainment"
    education = "Education"
    other = "Other"


class IncomeSource(str, Enum):
    salary = "Salary"
    freelancing = "Freelancing"
    business = "Business"
    other = "Other"


class DebtStatus(str, Enum):
    pending = "Pending"
    paid = "Paid"
    overdue = "Overdue"


class DebtType(str, Enum):
    personal_loan = "Personal Loan"
    emi = "EMI"
    friend_borrowed = "Borrowed From Friend"
    family_borrowed = "Borrowed From Family"
    lent_to_other = "Lent To Other"
