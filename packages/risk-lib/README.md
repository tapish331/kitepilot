# Kitepilot Risk Library

`kitepilot-risk` provides a reusable policy model and pure functions to evaluate
trading orders against pre-trade risk controls.

This library is intentionally framework agnostic and relies only on Pydantic
for type-safe models. It is consumed by the `risk-svc` FastAPI application and
the backtester.
