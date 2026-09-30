# AI-Based Multi-Agent Traffic Intelligence System

Prototype for predictive urban congestion management across four independent junction agents: J1, J2, J3, and J4.

## Phase 1 status

Phase 1 established the project structure, Python environment, FastAPI service, SQLite junction registry, and React/Vite/Tailwind dashboard shell. Phase 2 adds a deterministic synthetic dataset, SQLite traffic-state records, and read-only traffic APIs. The dashboard uses clearly labeled `DEMO DATA`; no real CCTV, trained model, or signal control is claimed.

## Structure

- `backend/app`: FastAPI service, database session, and SQLAlchemy models.
- `frontend/src`: React dashboard shell and API-connected components.
- `datasets`: Generated and imported traffic datasets in later phases.
- `scripts`: Dataset generation and model-training scripts in later phases.
- `trained_models`: Saved model artifacts in later phases.
- `simulation`: SUMO integration or Python fallback in later phases.
- `datasets/synthetic_traffic.csv`: generated 15-minute records for J1-J4.

## Run the backend

Open Terminal 1 in this folder:

```powershell
.\venv\Scripts\Activate.ps1
cd backend
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive docs are at `http://127.0.0.1:8000/docs`.

## Run the frontend

Node.js/npm must be installed first. Open Terminal 2:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally `http://127.0.0.1:5173`.

## Phase 1 checks

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/health
Invoke-RestMethod http://127.0.0.1:8000/api/junctions
Invoke-RestMethod http://127.0.0.1:8000/api/traffic-state
Invoke-RestMethod 'http://127.0.0.1:8000/api/analytics?junction_id=J3&limit=24'
Invoke-RestMethod http://127.0.0.1:8000/api/predictions
```

Expected junction and traffic-state responses contain J1, J2, J3, and J4 with `mode: DEMO DATA`. Prediction responses explicitly show `MODEL_NOT_TRAINED` until Phase 4.

Regenerate the dataset:

```powershell
..\venv\Scripts\python.exe scripts\generate_data.py --days 14 --output datasets\synthetic_traffic.csv
```

## Next phase

Phase 3 will add the independent J1-J4 junction agents and simple agent-to-agent communication.
