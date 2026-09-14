# AmberFlux AI Engineering Internship Assignment

A production-minded FastAPI backend for analyzing unstructured customer quotation requests and recommending deterministic follow-up actions based on CRM information.

## Overview

This project implements two backend APIs:

1. `POST /analyze-request`
   - Converts an unstructured customer message into structured quotation-request data.
   - Uses an LLM for language understanding and extraction.
   - Validates and normalizes the result using Pydantic and deterministic backend logic.

2. `POST /recommend-action`
   - Recommends the next business action using CRM information.
   - Uses deterministic Python business rules instead of an LLM.

The implementation focuses on clear separation between:
- API layer
- LLM/extraction layer
- Data validation
- Business rules
- Reliability and error handling

---

## Architecture

```text
                    Customer Message
                           |
                           v
                    FastAPI Endpoint
                           |
                           v
                  Extraction Service
                           |
                           v
                      LLM Service
                           |
                           v
                  Structured JSON
                           |
                           v
                 Pydantic Validation
                           |
                           v
             Missing Fields + Confidence
                           |
                           v
                    API Response


CRM Information
      |
      v
FastAPI /recommend-action
      |
      v
Recommendation Service
      |
      v
Deterministic Business Rules
      |
      v
Action + Priority + Reason