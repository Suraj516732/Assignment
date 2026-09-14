from app.business.rules import recommend_action


def test_customer_replied():
    action, priority, reason = recommend_action(
        existing_customer=True,
        quote_sent=True,
        days_since_quote=2,
        last_customer_contact_days=2,
        customer_replied=True,
    )

    assert action == "Respond to customer"
    assert priority == "high"


def test_old_quote_requires_high_priority_follow_up():
    action, priority, reason = recommend_action(
        existing_customer=False,
        quote_sent=True,
        days_since_quote=8,
        last_customer_contact_days=8,
        customer_replied=False,
    )

    assert action == "Follow up on quotation"
    assert priority == "high"


def test_recent_quote_requires_medium_priority_follow_up():
    action, priority, reason = recommend_action(
        existing_customer=True,
        quote_sent=True,
        days_since_quote=5,
        last_customer_contact_days=5,
        customer_replied=False,
    )

    assert action == "Follow up on quotation"
    assert priority == "medium"


def test_unknown_existing_customer_status():
    action, priority, reason = recommend_action(
        existing_customer=None,
        quote_sent=False,
        days_since_quote=None,
        last_customer_contact_days=2,
        customer_replied=False,
    )

    assert action == "Review CRM information"
    assert priority == "low"


def test_no_immediate_action():
    action, priority, reason = recommend_action(
        existing_customer=False,
        quote_sent=False,
        days_since_quote=None,
        last_customer_contact_days=2,
        customer_replied=False,
    )

    assert action == "Monitor lead"
    assert priority == "low"