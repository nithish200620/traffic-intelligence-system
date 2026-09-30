import csv
from datetime import datetime
from pathlib import Path

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.database.session import Base, engine, get_db
from app.models import Junction, TrafficState

app = FastAPI(
    title="AI Traffic Intelligence Center",
    version="0.1.0",
    description="Phase 1 foundation for the four-junction traffic intelligence prototype.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def initialize_database():
    Base.metadata.create_all(bind=engine)
    with next(get_db()) as database:
        existing = database.scalars(select(Junction)).all()
        if not existing:
            database.add_all(
                [
                    Junction(junction_id=f"J{number}", name=f"Junction {number}")
                    for number in range(1, 5)
                ]
            )
            database.commit()
        if not database.scalar(select(TrafficState.id).limit(1)):
            dataset_path = Path(__file__).resolve().parents[2] / "datasets" / "synthetic_traffic.csv"
            if dataset_path.exists():
                with dataset_path.open(newline="", encoding="utf-8") as dataset_file:
                    rows = csv.DictReader(dataset_file)
                    database.add_all(
                        TrafficState(
                            timestamp=datetime.fromisoformat(row["timestamp"]),
                            junction_id=row["junction_id"],
                            vehicle_count=int(row["vehicle_count"]),
                            average_speed=float(row["average_speed"]),
                            queue_length=float(row["queue_length"]),
                            density=float(row["density"]),
                            traffic_flow=float(row["traffic_flow"]),
                            movement_utilization=float(row["movement_utilization"]),
                            congestion_score=float(row["congestion_score"]),
                            congestion_category=row["congestion_category"],
                            weather=row["weather"],
                        )
                        for row in rows
                    )
                database.commit()


initialize_database()


@app.get("/api/health")
def health_check():
    return {"status": "ok", "phase": 1, "mode": "foundation"}


@app.get("/api/junctions")
def list_junctions(database: Session = Depends(get_db)):
    junctions = database.scalars(select(Junction).order_by(Junction.junction_id)).all()
    return {
        "mode": "DEMO DATA",
        "items": [
            {
                "junction_id": junction.junction_id,
                "name": junction.name,
                "status": junction.status,
            }
            for junction in junctions
        ],
    }


def serialize_state(state: TrafficState) -> dict:
    return {
        "timestamp": state.timestamp.isoformat(),
        "junction_id": state.junction_id,
        "vehicle_count": state.vehicle_count,
        "average_speed": state.average_speed,
        "queue_length": state.queue_length,
        "density": state.density,
        "traffic_flow": state.traffic_flow,
        "movement_utilization": state.movement_utilization,
        "congestion_score": state.congestion_score,
        "congestion_category": state.congestion_category,
        "weather": state.weather,
    }


def latest_states(database: Session, junction_id: str | None = None) -> list[TrafficState]:
    query = select(TrafficState).order_by(desc(TrafficState.timestamp))
    if junction_id:
        query = query.where(TrafficState.junction_id == junction_id.upper())
    states = database.scalars(query).all()
    latest_by_junction = {}
    for state in states:
        latest_by_junction.setdefault(state.junction_id, state)
    return list(latest_by_junction.values())


@app.get("/api/traffic-state")
def traffic_state(
    junction_id: str | None = Query(default=None, pattern="^J[1-4]$"),
    database: Session = Depends(get_db),
):
    return {"mode": "DEMO DATA", "items": [serialize_state(state) for state in latest_states(database, junction_id)]}


@app.get("/api/predictions")
def predictions(junction_id: str | None = Query(default=None, pattern="^J[1-4]$"), database: Session = Depends(get_db)):
    return {
        "model_status": "MODEL_NOT_TRAINED",
        "message": "Train the XGBoost model in a later phase before showing predictions.",
        "items": [{"junction_id": state.junction_id, "predicted_congestion_score": None, "category": None} for state in latest_states(database, junction_id)],
    }


@app.get("/api/events")
def events(database: Session = Depends(get_db)):
    return {
        "mode": "DEMO DATA",
        "items": [],
        "message": "Event detection will be populated from behavior analysis in a later phase.",
    }


@app.get("/api/recommendations")
def recommendations():
    return {
        "status": "MODEL_NOT_TRAINED",
        "items": [],
        "message": "Recommendations are unavailable until agent coordination and prediction are implemented.",
    }


@app.get("/api/agents")
def agents():
    return {"status": "PHASE_2_PENDING", "items": [], "message": "Junction agents arrive in Phase 3."}


@app.get("/api/emergency")
def emergency():
    return {"status": "DEMO_DATA_PENDING", "ambulance_detected": False, "message": "Emergency detection requires the vision phase."}


@app.get("/api/analytics")
def analytics(
    junction_id: str = Query(default="J1", pattern="^J[1-4]$"),
    limit: int = Query(default=48, ge=1, le=200),
    database: Session = Depends(get_db),
):
    states = database.scalars(
        select(TrafficState)
        .where(TrafficState.junction_id == junction_id)
        .order_by(desc(TrafficState.timestamp))
        .limit(limit)
    ).all()
    return {"mode": "DEMO DATA", "junction_id": junction_id, "items": [serialize_state(state) for state in reversed(states)]}
