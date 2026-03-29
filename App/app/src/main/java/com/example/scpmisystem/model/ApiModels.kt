package com.example.scpmisystem.model

data class AuthRequest(
    val username: String,
    val password: String
)

data class AuthResponse(
    val message: String
)


//  recommend response (district-based + price)
data class RecommendResponse(
    val district: String,
    val crop: String,
    val estimated_price: Double?,
    val reason: String
)



//mandi response (district → crop → price)

data class MandiResponse(
    val state: String,
    val district: String,
    val season: String,
    val crop: String,
    val estimated_price: Double?,
    val latest_price_column: String?,
    val label: String
)


// production (state-level only)
data class ProductionResponse(
    val state: String,
    val production: Double?,
    val demand: Double?,
    val demand_gap: Double?,
    val status: String
)


// predict response
data class PredictResponse(
    val state: String,
    val district: String,
    val season: String,
    val crop: String,
    val area: Double,
    val predicted_yield: Double,
    val confidence: Double
)
