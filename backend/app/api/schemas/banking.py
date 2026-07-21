from enum import Enum

from pydantic import BaseModel, Field


class TransactionType(str, Enum):

    BALANCE_CHECK = "BALANCE_CHECK"

    LOCAL_TRANSFER = "LOCAL_TRANSFER"

    INTERNATIONAL_TRANSFER = "INTERNATIONAL_TRANSFER"

    BILL_PAYMENT = "BILL_PAYMENT"

    LOAN_PAYMENT = "LOAN_PAYMENT"

    HIGH_VALUE_TRANSFER = "HIGH_VALUE_TRANSFER"


class BankingRequest(BaseModel):

    transaction_type: TransactionType

    amount: float = Field(..., ge=0)

    trusted_device: bool

    authenticated: bool
