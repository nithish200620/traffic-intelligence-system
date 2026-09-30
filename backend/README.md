# Traffic Intelligence Backend

Phases 1 and 2 provide the FastAPI service, SQLite database, four-junction registry, synthetic traffic-state records, and read-only analytics endpoints.

Run from the `backend` directory:

```powershell
..\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Check `http://127.0.0.1:8000/docs` for the generated API documentation.

Phase 2 endpoints include `/api/traffic-state`, `/api/analytics`, `/api/events`, `/api/recommendations`, `/api/agents`, `/api/emergency`, and `/api/predictions`. Prediction-dependent endpoints report `MODEL_NOT_TRAINED` until the XGBoost phase is implemented.
