package com.example.scpmisystem.model

data class AuthRequest(
    val username: String,
    val password: String
)

data class AuthResponse(
    val message: String
)


// ✅ UPDATED: recommend response (district-based + price)
data class RecommendResponse(
    val district: String,
    val recommended_crop: String,
    val estimated_price: Double,
    val reason: String
)



// ✅ NEW mandi response (district → crop → price)

data class MandiResponse(
    val district: String,
    val crop: String,
    val price: Double,
    val type: String
)


// ✅ UPDATED production (state-level only)
data class ProductionResponse(
    val state: String,
    val production: Double,
    val demand: Double,
    val gap: Double,
    val status: String
)


// ✅ UPDATED predict response
data class PredictResponse(
    val district: String,
    val crop: String,
    val area: Double,
    val predicted_yield: String
)