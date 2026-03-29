from .dataset_loader import load_crop_data
from .mandi_analysis import get_crop_price_estimate


def recommend_crop(state: str, district: str, season: str) -> dict:
    df = load_crop_data()
    filtered = df[
        (df["State_Name_norm"] == state.strip().lower())
        & (df["District_Name_norm"] == district.strip().lower())
        & (df["Season_norm"] == season.strip().lower())
    ]
    if filtered.empty:
        return {
            "district": district.strip(),
            "crop": None,
            "estimated_price": None,
            "reason": "No district-level crop data found for the selected filters.",
        }

    grouped = filtered.groupby("Crop", as_index=False)["Production"].max()
    best_row = grouped.sort_values(["Production", "Crop"], ascending=[False, True]).iloc[0]
    top_crop = str(best_row["Crop"]).strip()
    production = float(best_row["Production"])
    price_summary = get_crop_price_estimate(top_crop, district)

    return {
        "district": district.strip(),
        "crop": top_crop,
        "estimated_price": price_summary["estimated_price"],
        "reason": f"Recommended because {top_crop} has the highest district-level production ({round(production, 2)}) in {district.strip()} for {season.strip()}.",
    }
