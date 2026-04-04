from pydantic import BaseModel
from typing import Optional

class ReleaseCreate(BaseModel):
    name: str
    description: str

class BADecision(BaseModel):
    status: str  # approved or rejected
    comment: Optional[str] = ""

class MetricsCheck(BaseModel):
    pre_metrics: dict
    post_metrics: dict