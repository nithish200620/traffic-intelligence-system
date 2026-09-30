from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

JUNCTIONS = ("J1", "J2", "J3", "J4")
WEATHER = ("clear", "rain")


def congestion_category(score: float) -> str:
    if score < 25:
        return "LOW"
    if score < 50:
        return "MODERATE"
    if score < 75:
        return "HIGH"
    return "CRITICAL"


def generate_dataset(days: int = 14, seed: int = 42) -> pd.DataFrame:
    generator = np.random.default_rng(seed)
    timestamps = pd.date_range(
        end=pd.Timestamp.now().floor("15min"), periods=days * 24 * 4, freq="15min"
    )
    rows = []
    junction_factor = {"J1": 1.00, "J2": 0.86, "J3": 1.18, "J4": 0.94}

    for timestamp in timestamps:
        hour = timestamp.hour + timestamp.minute / 60
        weekend = timestamp.dayofweek >= 5
        morning_peak = 7 <= hour < 10
        evening_peak = 16 <= hour < 20
        peak_factor = 1.45 if morning_peak or evening_peak else 0.72 if 11 <= hour < 15 else 0.9
        day_factor = 0.68 if weekend else 1.0
        weather = "rain" if generator.random() < (0.16 if not weekend else 0.22) else "clear"
        event_indicator = int(generator.random() < 0.035)

        for junction_id in JUNCTIONS:
            factor = junction_factor[junction_id]
            base_count = 42 * factor * peak_factor * day_factor
            vehicle_count = max(4, int(generator.normal(base_count * (1.25 if event_indicator else 1), 5)))
            bike_share = 0.24 if weather == "clear" else 0.15
            bike_count = max(0, int(generator.normal(vehicle_count * bike_share, 2)))
            bus_count = max(0, int(generator.normal(vehicle_count * 0.08, 1)))
            truck_count = max(0, int(generator.normal(vehicle_count * 0.06, 1)))
            car_count = max(0, vehicle_count - bike_count - bus_count - truck_count)
            ambulance_count = int(generator.random() < 0.018)
            average_speed = float(np.clip(generator.normal(42 - vehicle_count * 0.25 - (8 if weather == "rain" else 0), 3), 5, 55))
            density = float(np.clip(vehicle_count / (55 * factor), 0, 1.5))
            queue_length = float(np.clip(vehicle_count * max(0.2, 1 - average_speed / 55) * 2.8, 0, 260))
            traffic_flow = float(np.clip(vehicle_count * average_speed * 0.42, 0, 1600))
            movement_utilization = float(np.clip(0.35 + density * 0.45 + generator.normal(0, 0.04), 0, 1))
            bus_activity = float(np.clip(bus_count / max(vehicle_count, 1) * 4, 0, 1))
            abnormal_activity = int(generator.random() < (0.05 + 0.08 * event_indicator))
            previous_congestion = float(np.clip(density * 62 + generator.normal(0, 5), 0, 100))
            congestion_score = float(np.clip(
                density * 48 + max(0, 35 - average_speed) * 1.2 + queue_length * 0.12
                + event_indicator * 8 + (7 if weather == "rain" else 0) + generator.normal(0, 3),
                0,
                100,
            ))
            rows.append({
                "timestamp": timestamp.isoformat(),
                "junction_id": junction_id,
                "vehicle_count": vehicle_count,
                "car_count": car_count,
                "bike_count": bike_count,
                "bus_count": bus_count,
                "truck_count": truck_count,
                "ambulance_count": ambulance_count,
                "average_speed": round(average_speed, 2),
                "queue_length": round(queue_length, 2),
                "density": round(density, 4),
                "traffic_flow": round(traffic_flow, 2),
                "movement_utilization": round(movement_utilization, 4),
                "bus_activity": round(bus_activity, 4),
                "abnormal_activity": abnormal_activity,
                "weather": weather,
                "event_indicator": event_indicator,
                "previous_congestion": round(previous_congestion, 2),
                "congestion_score": round(congestion_score, 2),
                "congestion_category": congestion_category(congestion_score),
            })
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic four-junction traffic data.")
    parser.add_argument("--days", type=int, default=14)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("datasets/synthetic_traffic.csv"))
    args = parser.parse_args()
    dataframe = generate_dataset(days=args.days, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(args.output, index=False)
    print(f"Generated {len(dataframe):,} synthetic records at {args.output}")


if __name__ == "__main__":
    main()
