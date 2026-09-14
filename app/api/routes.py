from fastapi import APIRouter, HTTPException

from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
)
from app.services.extraction_service import analyze_customer_request
from app.services.recommendation_service import get_recommendation

from app.services.idempotency_service import (
    get_processed_request,
    save_processed_request,
)

router = APIRouter()

@router.post(
    "/analyze-request",
    response_model=AnalyzeResponse,
)
async def analyze_request(request: AnalyzeRequest):

    # Check if this request was already processed
    cached_result = get_processed_request(request.request_id)

    if cached_result is not None:
        return cached_result

    try:
        result = await analyze_customer_request(
            request_id=request.request_id,
            message=request.message,
        )

        # Save successful result for future duplicate requests
        save_processed_request(
            request.request_id,
            result,
        )

        return result

    except (ValueError, RuntimeError) as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        ) from exc

@router.post(
    "/recommend-action",
    response_model=RecommendationResponse,
)
async def recommend_action(request: RecommendationRequest):

    try:
        return get_recommendation(request)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        ) from exc