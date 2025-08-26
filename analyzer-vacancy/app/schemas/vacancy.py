from pydantic import BaseModel, field_validator, ConfigDict
from typing import List
from datetime import date, datetime

class VacancyBase(BaseModel):
    title: str
    description: str
    skills: List[str]
    published_at: str
    
class VacancyCreate(VacancyBase):

    model_config = ConfigDict(from_attributes=True)

class VacancyOut(VacancyBase):
    id: int
    work_format: str
    url: str
    
    model_config = ConfigDict(from_attributes=True)

    @field_validator("published_at", mode="before")
    @classmethod
    def validate_date(cls, v):
        if not v: return ''
        elif isinstance(v, (datetime, date)):
            return v.strftime("%d.%m.%Y")
        return v


