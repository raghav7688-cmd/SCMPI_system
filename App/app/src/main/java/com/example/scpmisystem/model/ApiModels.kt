package com.example.scpmisystem.model

data class AuthRequest(
    val username: String,
    val password: String
)

data class AuthResponse(
    val message: String
)

data class RecommendResponse(
    val recommended_crop: String,
    val expected_production: Double,
    val confidence: Double
)

data class MarketItem(
    val city: String,
    val commodity: String,
    val group: String,
    val msp: Double,
    val latest_price: Double?,
    val latest_arrival: Double?,
    val prices: Map<String, Double>,
    val arrivals: Map<String, Double>
)

data class MarketsResponse(
    val markets: List<MarketItem>
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