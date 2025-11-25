from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class OperatorBase(BaseModel):
    name: str
    is_active: bool = True
    leads_limit: int = 10

class OperatorCreate(OperatorBase):
    pass

class OperatorCreate(OperatorBase):
    pass

class OperatorUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None
    leads_limit: int | None
    
class OperatorRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)    



class LeadBase(BaseModel):
    external_lead_id: str
    name: str | None = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    external_lead_id: str | None = None
    name: str | None = None

class LeadRead(LeadBase):
    id: int
    contacts: list["ContactRead"] = []

    model_config = ConfigDict(from_attributes=True)


class SourceBase(BaseModel):
    name: str

class SourceCreate(SourceBase):
    pass

class SourceUpdate(BaseModel):
    name: str | None = None

class SourceRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class OperatorSourceWeightBase(BaseModel):
    operator_id: int
    source_id: int
    weight: float = Field(gt=0)

class OperatorSourceWeightCreate(BaseModel):
    operator_id: int
    weight: float = Field(gt=0)

class OperatorSourceWeightUpdate(BaseModel):
    weight: float | None = Field(default=None, gt=0)

class OperatorSourceWeightRead(OperatorSourceWeightBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ContactBase(BaseModel):
    message: str | None = None
    is_active: bool = True

class ContactCreate(ContactBase):
    external_lead_id: int 
    source_id: int 

class ContactUpdate(BaseModel):
    message: str | None = None
    is_active: bool | None = None
    operator_id: int | None = None

class ContactRead(ContactBase):
    id: int
    created_at: datetime

    external_lead_id: int
    source_id: int
    operator_id: int | None

    source: "SourceRead"
    operator: OperatorRead | None

    model_config = ConfigDict(from_attributes=True)


class OperatorDistributionRead(BaseModel):
    operator_id: int
    operator_name: str
    total_contacts: int
    by_source: dict[str, int]