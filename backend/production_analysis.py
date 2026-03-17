from .dataset_loader import load_state_supply_data


def production_vs_demand(state: str) -> dict:
    df = load_state_supply_data()
    row = df[df["State"].str.lower() == state.lower()]
    if row.empty:
        return {"state": state, "production": None, "national_average": None, "status": "unknown"}
    production = float(row.iloc[0]["Production_TotalFoodgrains"])
    demand = float(row["Demand_Proxy_TotalFoodgrains"].mean())
    status = "Balanced Production"
    if production > 1.1 * demand:
        status = "High Production"
    elif production < 0.9 * demand:
        status = "Low Production"
    return {
        "state": state,
        "production": round(production, 2),
        "national_average": round(demand, 2),
        "status": status,
    }

