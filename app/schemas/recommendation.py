from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    request_id: str = Field(..., min_length=1)

    lead_type: str | None = None

    existing_customer: bool | None = None

    quote_sent: bool = False

    days_since_quote: int | None = Field(default=None, ge=0)

    last_customer_contact_days: int | None = Field(default=None, ge=0)

    customer_replied: bool = False


class RecommendationResponse(BaseModel):
    request_id: str

    recommended_action: str

    priority: str

    reason: str