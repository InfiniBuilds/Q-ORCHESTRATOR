from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True)
class BankingTransaction:
    transaction_id: str
    sender_id: str
    receiver_id: str
    amount: Decimal
    currency: str
    timestamp_ms: int

    def __post_init__(self):
        if not self.transaction_id:
            raise ValueError("transaction_id is required")

        if not self.sender_id:
            raise ValueError("sender_id is required")

        if not self.receiver_id:
            raise ValueError("receiver_id is required")

        if self.sender_id == self.receiver_id:
            raise ValueError(
                "sender and receiver must be different"
            )

        try:
            amount = Decimal(self.amount)
        except InvalidOperation as exc:
            raise ValueError("invalid amount") from exc

        if amount <= Decimal("0"):
            raise ValueError(
                "transaction amount must be positive"
            )

        if len(self.currency) != 3:
            raise ValueError(
                "currency must use a 3-letter code"
            )

        if self.timestamp_ms <= 0:
            raise ValueError(
                "timestamp_ms must be positive"
            )
