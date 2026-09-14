from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    request_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class AnalyzeResponse(BaseModel):
    request_id: str

    customer_name: str | None = None
    company: str | None = None
    customer_type: str | None = None
    project_address: str | None = None
    product: str | None = None
    dimensions: str | None = None
    requested_timeline: str | None = None
    requirements: str | None = None

    missing_information: list[str] = Field(default_factory=list)

    confidence: float = Field(ge=0.0, le=1.0)

    summary: str