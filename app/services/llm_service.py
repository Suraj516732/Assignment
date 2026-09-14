from openai import AsyncOpenAI

from app.core.config import OPENAI_API_KEY, OPENAI_MODEL


if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not configured")


client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
)


async def extract_customer_request(message: str) -> str:
    try:
        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": """
You extract structured information from customer quotation requests.

Return only valid JSON.

Extract:
- customer_name
- company
- customer_type
- project_address
- product
- dimensions
- requested_timeline
- requirements
- missing_information
- summary

Rules:
- Do not invent information.
- Use null when a field is not available.
- missing_information must be a list of field names.
- Ignore irrelevant information.
- If information conflicts, preserve the uncertainty rather than guessing.
""",
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("LLM returned an empty response")

        return content

    except Exception as exc:
        raise RuntimeError(
            "LLM provider request failed"
        ) from exc