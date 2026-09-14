def recommend_action(
    existing_customer: bool | None,
    quote_sent: bool,
    days_since_quote: int | None,
    last_customer_contact_days: int | None,
    customer_replied: bool,
) -> tuple[str, str, str]:

    # Highest priority: customer has replied
    if customer_replied:
        return (
            "Respond to customer",
            "high",
            "Customer has replied and requires a timely response.",
        )

    # Quote has been sent and customer has not replied
    if quote_sent and days_since_quote is not None:

        if days_since_quote >= 7:
            return (
                "Follow up on quotation",
                "high",
                "Quotation has been pending for 7 or more days without a customer reply.",
            )

        if days_since_quote >= 3:
            return (
                "Follow up on quotation",
                "medium",
                "Quotation was sent several days ago and the customer has not replied.",
            )

    # No recent contact
    if (
        last_customer_contact_days is not None
        and last_customer_contact_days >= 7
    ):
        return (
            "Contact customer",
            "medium",
            "Customer has not been contacted for 7 or more days.",
        )

    # CRM uncertainty
    if existing_customer is None:
        return (
            "Review CRM information",
            "low",
            "Existing-customer status is unknown in the CRM.",
        )

    # Existing customer without urgent activity
    if existing_customer:
        return (
            "Maintain customer relationship",
            "low",
            "Existing customer has no immediate follow-up requirement.",
        )

    # Default
    return (
        "Monitor lead",
        "low",
        "No immediate follow-up action is required.",
    )