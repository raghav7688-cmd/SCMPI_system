from .dataset_loader import load_state_supply_data


def production_vs_demand(state: str) -> dict:
    df = load_state_supply_data()
    row = df[df["State_norm"] == state.strip().lower()]
    if row.empty:
        return {
            "state": state.strip(),
            "production": None,
            "demand": None,
            "demand_gap": None,
            "status": "unknown",
        }

    production = float(row.iloc[0]["Production"])
    demand = float(row.iloc[0]["Demand"])
    demand_gap = round(demand - production, 2)

    if demand_gap > 0:
        status = "High"
    elif abs(demand_gap) <= max(demand * 0.1, 1):
        status = "Balanced"
    else:
        status = "Surplus"

    return {
        "state": state.strip(),
        "production": round(production, 2),
        "demand": round(demand, 2),
        "demand_gap": demand_gap,
        "status": status,
    }
