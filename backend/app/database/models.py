from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class OrchestrationLog(Base):
    __tablename__ = "orchestration_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    # -----------------------------
    # Request Context
    # -----------------------------

    domain: Mapped[str] = mapped_column(
        String(30)
    )

    # -----------------------------
    # Security Decision
    # -----------------------------

    security_score: Mapped[float] = mapped_column(
        Float
    )

    security_rank: Mapped[str] = mapped_column(
        String(30)
    )

    triggered_rule: Mapped[str] = mapped_column(
        String(50)
    )

    # -----------------------------
    # Resource Decision
    # -----------------------------

    resource_score: Mapped[float] = mapped_column(
        Float
    )

    resource_capability: Mapped[str] = mapped_column(
        String(20)
    )

    # -----------------------------
    # Selected Profile
    # -----------------------------

    selected_profile: Mapped[str] = mapped_column(
        String(30)
    )

    # -----------------------------
    # Algorithms
    # -----------------------------

    mlkem_algorithm: Mapped[str] = mapped_column(
        String(30)
    )

    mldsa_algorithm: Mapped[str] = mapped_column(
        String(30)
    )

    hybrid_enabled: Mapped[bool] = mapped_column(
        Boolean
    )

    # -----------------------------
    # Crypto Result
    # -----------------------------

    signature_verified: Mapped[bool] = mapped_column(
        Boolean
    )

    ciphertext_size: Mapped[int] = mapped_column(
        Integer
    )

    session_key_size: Mapped[int] = mapped_column(
        Integer
    )

    execution_time_ms: Mapped[float] = mapped_column(
        Float
    )
