import json
from decimal import Decimal

from app.banking.transaction import BankingTransaction


def _canonical_decimal(value: Decimal) -> str:
    normalized = value.normalize()

    result = format(normalized, "f")

    if "." in result:
        result = result.rstrip("0").rstrip(".")

    return result


def canonicalize_transaction(
    transaction: BankingTransaction,
) -> bytes:
    payload = {
        "amount": _canonical_decimal(transaction.amount),
        "currency": transaction.currency.upper(),
        "receiver_id": transaction.receiver_id,
        "sender_id": transaction.sender_id,
        "timestamp_ms": transaction.timestamp_ms,
        "transaction_id": transaction.transaction_id,
    }

    canonical_json = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    return canonical_json.encode("utf-8")
