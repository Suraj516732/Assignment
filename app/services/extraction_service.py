import json

from app.schemas.analyze import AnalyzeResponse
from app.services.llm_service import extract_customer_request


IMPORTANT_FIELDS = [
    "customer_name",
    "company",
    "customer_type",
    "project_address",
    "product",
    "dimensions",
    "requested_timeline",
]


async def analyze_customer_request(
    request_id: str,
    message: str,
) -> AnalyzeResponse:

    # Step 1: Send customer message to LLM
    raw_result = await extract_customer_request(message)

    # Step 2: Parse LLM JSON response
    try:
        data = json.loads(raw_result)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM returned invalid JSON") from exc

    # Step 3: Safely normalize missing_information
    missing_information = data.get("missing_information") or []

    if isinstance(missing_information, dict):
        missing_information = [
            field
            for field, value in missing_information.items()
            if value is None or value == ""
        ]

    elif isinstance(missing_information, str):
        missing_information = [missing_information]

    elif not isinstance(missing_information, list):
        missing_information = []

    # Step 4: Detect missing important fields ourselves
    # We don't blindly trust the LLM's missing_information.
    for field in IMPORTANT_FIELDS:
        value = data.get(field)

        if value is None or str(value).strip() == "":
            if field not in missing_information:
                missing_information.append(field)

    # Step 5: Calculate deterministic confidence
    available_fields = sum(
        1
        for field in IMPORTANT_FIELDS
        if data.get(field) is not None
        and str(data.get(field)).strip() != ""
    )

    confidence = available_fields / len(IMPORTANT_FIELDS)

    # Step 6: Validate final response using Pydantic
    return AnalyzeResponse(
        request_id=request_id,
        customer_name=data.get("customer_name"),
        company=data.get("company"),
        customer_type=data.get("customer_type"),
        project_address=data.get("project_address"),
        product=data.get("product"),
        dimensions=data.get("dimensions"),
        requested_timeline=data.get("requested_timeline"),
        requirements=data.get("requirements"),
        missing_information=missing_information,
        confidence=round(confidence, 2),
        summary=data.get("summary", ""),
    )