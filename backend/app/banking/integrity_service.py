from dataclasses import dataclass

from app.banking.canonical import canonicalize_transaction
from app.banking.signing_identity import (
    BankingSignature,
    BankingSigningIdentity,
)
from app.banking.transaction import BankingTransaction


@dataclass(frozen=True)
class SignedBankingTransaction:
    transaction: BankingTransaction
    canonical_payload: bytes
    signature: BankingSignature


class BankingIntegrityService:
    def __init__(
        self,
        signing_identity: BankingSigningIdentity,
    ):
        self.signing_identity = signing_identity

    def sign_transaction(
        self,
        transaction: BankingTransaction,
    ) -> SignedBankingTransaction:
        canonical_payload = canonicalize_transaction(
            transaction
        )

        signature = self.signing_identity.sign(
            canonical_payload
        )

        return SignedBankingTransaction(
            transaction=transaction,
            canonical_payload=canonical_payload,
            signature=signature,
        )

    def verify_transaction(
        self,
        signed_transaction: SignedBankingTransaction,
    ) -> bool:
        expected_payload = canonicalize_transaction(
            signed_transaction.transaction
        )

        if (
            expected_payload
            != signed_transaction.canonical_payload
        ):
            return False

        return self.signing_identity.verify(
            message=expected_payload,
            signature=signed_transaction.signature,
        )
