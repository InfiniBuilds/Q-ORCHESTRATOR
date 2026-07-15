from decimal import Decimal

from app.banking.canonical import canonicalize_transaction
from app.banking.integrity_service import (
    BankingIntegrityService,
    SignedBankingTransaction,
)
from app.banking.signing_identity import BankingSigningIdentity
from app.banking.transaction import BankingTransaction


def create_transaction(
    amount: Decimal,
) -> BankingTransaction:
    return BankingTransaction(
        transaction_id="TXN-001",
        sender_id="USER001",
        receiver_id="USER002",
        amount=amount,
        currency="INR",
        timestamp_ms=1784080000000,
    )


def test_canonicalization():
    print("\n=== Testing canonical transaction encoding ===")

    transaction_a = create_transaction(
        Decimal("50000.00")
    )

    transaction_b = create_transaction(
        Decimal("50000")
    )

    payload_a = canonicalize_transaction(transaction_a)
    payload_b = canonicalize_transaction(transaction_b)

    if payload_a != payload_b:
        raise RuntimeError(
            "Equivalent amounts produced different bytes"
        )

    print("Deterministic encoding : PASS")
    print("Canonical payload      :", payload_a.decode())


def test_signature_and_tampering():
    print("\n=== Testing banking ML-DSA integrity ===")

    identity = BankingSigningIdentity(
        signer_id="BANK-SERVER-001",
        algorithm="ML-DSA-65",
    )

    service = BankingIntegrityService(identity)

    original_transaction = create_transaction(
        Decimal("50000")
    )

    signed_transaction = service.sign_transaction(
        original_transaction
    )

    valid = service.verify_transaction(
        signed_transaction
    )

    if not valid:
        raise RuntimeError(
            "Valid banking transaction rejected"
        )

    tampered_transaction = create_transaction(
        Decimal("500000")
    )

    tampered_signed_transaction = SignedBankingTransaction(
        transaction=tampered_transaction,
        canonical_payload=signed_transaction.canonical_payload,
        signature=signed_transaction.signature,
    )

    tampered_valid = service.verify_transaction(
        tampered_signed_transaction
    )

    if tampered_valid:
        raise RuntimeError(
            "Tampered banking transaction accepted"
        )

    print("Valid transaction      : PASS")
    print("Amount tamper rejection : PASS")
    print(
        "Signature size         :",
        len(signed_transaction.signature.signature),
        "bytes",
    )


if __name__ == "__main__":
    test_canonicalization()
    test_signature_and_tampering()

    print("\nALL BANKING INTEGRITY TESTS PASSED")
