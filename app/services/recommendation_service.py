from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
)
from app.business.rules import recommend_action


def get_recommendation(
    request: RecommendationRequest,
) -> RecommendationResponse:

    action, priority, reason = recommend_action(
        existing_customer=request.existing_customer,
        quote_sent=request.quote_sent,
        days_since_quote=request.days_since_quote,
        last_customer_contact_days=request.last_customer_contact_days,
        customer_replied=request.customer_replied,
    )

    return RecommendationResponse(
        request_id=request.request_id,
        recommended_action=action,
        priority=priority,
        reason=reason,
    )
    