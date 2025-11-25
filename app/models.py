from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Float, Boolean, UniqueConstraint, func
from sqlalchemy.orm import relationship, Mapped, mapped_column


from app.database import Base


class Operator(Base):
    __tablename__ = "operators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="False")
    leads_limit: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

    contacts: Mapped[list["Contact"]] = relationship(back_populates="operator")
    sources_weights: Mapped[list["OperatorSourceWeight"]] = relationship(back_populates="operator", cascade="all, delete-orphan")

    def count_active_leads(self) -> int:
        return sum(1 for c in self.contacts if c.is_active)


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    operators_weights: Mapped[list["OperatorSourceWeight"]] = relationship(back_populates="source", cascade="all, delete-orphan")
    contacts: Mapped[list["Contact"]] = relationship(back_populates="source")


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String)

    external_lead_id: Mapped[str] = mapped_column(String, nullable=False) # Абстрактный внешний указатель лида, не зависящий от основного id (вполне можно объединить с id, но все зависит от бизнес логики)
    __table_args__ = (UniqueConstraint("external_lead_id", name="uq_lead_external_lead_id"),)

    contacts: Mapped[list["Contact"]] = relationship(back_populates="lead")


class Contact(Base):
    __tablename__ = "сontacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    external_lead_id: Mapped[int] = mapped_column(ForeignKey("leads.external_lead_id"))
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    operator_id: Mapped[int | None] = mapped_column(ForeignKey("operators.id"))

    message: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    lead: Mapped["Lead"] = relationship(back_populates="contacts")
    source: Mapped["Source"] = relationship(back_populates="contacts")
    operator: Mapped["Operator"] = relationship(back_populates="contacts")


class OperatorSourceWeight(Base):
    __tablename__ = "operator_source_weights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"))
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    weight: Mapped[float] = mapped_column(Float, nullable=False)

    operator: Mapped["Operator"] = relationship(back_populates="sources_weights")
    source: Mapped["Source"] = relationship(back_populates="operators_weights")

    __table_args__ = (
        UniqueConstraint("operator_id", "source_id",
                         name="uq_operator_source_unique"),
    )
