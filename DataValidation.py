from pydantic import BaseModel, EmailStr, AnyUrl, AnyHttpUrl, Field, field_validator, model_validator
from typing import Any, List, Dict, Optional, Annotated

class DataValidation(BaseModel):
    name: str = Field(max_length=60)
    city: str
    age: int=Field(gt=0, strict=True)
    gender: Optional[str]=None
    height: float=Field(gt=0, strict=True)
    weight: float=Field(gt=0, strict=True)
    bmi: float=Field(gt=0, strict=True)
    disease: str

    @field_validator('gender')
    @classmethod
    def validate(cls, value: Any):
        if value not in ['male', 'female']:
            raise ValueError()
        return value
    
    @model_validator(mode='after')
    def validate_gender(model):
        if model.disease == "skin" and model.gender is None:
            raise ValueError()
        else:
            return model

class DataValidationOptional(BaseModel):
    p_id: Annotated[Optional[str], Field(default=None, description="Enter the patient id")]
    name: Annotated[Optional[str], Field(default=None, description="name")]
    city: Annotated[Optional[str], Field(default=None, description="city")]
    age: Annotated[Optional[int], Field(default=None, gt=0, description="age")]
    gender: Annotated[Optional[str], Field(default=None, description="gender")]
    height: Annotated[Optional[float], Field(default=None, description="height")]
    weight: Annotated[Optional[float], Field(default=None, description="weight")]
    bmi: Annotated[Optional[float], Field(gt=0, default=None)]
    disease: Annotated[Optional[str], Field(default=None, description="disease")]
