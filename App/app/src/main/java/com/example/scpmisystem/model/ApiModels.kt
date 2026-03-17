package com.example.scpmisystem.model

data class RecommendResponse(
    val recommended_crop: String,
    val expected_production: Double,
    val confidence: Double
)

data class Market(
    val market: String,
    val state: String,
    val price: Double,
    val arrival: Double
)

data class MarketsResponse(
    val markets: List<Market>
)

data class ProductionResponse(
    val state: String,
    val production: Double?,
    val national_average: Double?,
    val status: String
)

data class PredictResponse(
    val predicted_yield: Double,
    val confidence: Double
)