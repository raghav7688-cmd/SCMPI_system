import pandas as pd
from .dataset_loader import load_mandi_data


def top_markets_for_crop(crop: str, limit: int = 5) -> list[dict]:
    df = load_mandi_data()

    filtered = df[df["Commodity"].str.lower() == crop.lower()]
    if filtered.empty:
        return []

    price_cols = [c for c in df.columns if c.startswith("Price_")]
    arrival_cols = [c for c in df.columns if c.startswith("Arrival_")]

    results = []

    for _, row in filtered.iterrows():
        prices = {col: float(row[col]) for col in price_cols if pd.notna(row[col])}
        arrivals = {col: float(row[col]) for col in arrival_cols if pd.notna(row[col])}

        latest_price = next(iter(prices.values()), None)
        latest_arrival = next(iter(arrivals.values()), None)

        results.append({
            "city": row.get("Market", "Unknown"),  #
            "commodity": row["Commodity"],
            "group": row.get("Commodity_Group", ""),
            "msp": float(row["MSP_2026_27"]),
            "latest_price": latest_price,
            "latest_arrival": latest_arrival,
            "prices": prices,
            "arrivals": arrivals,
        })

    #  Sort by highest price (top markets)
    results = sorted(results, key=lambda x: x["latest_price"] or 0, reverse=True)

    return results[:limit]