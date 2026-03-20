package com.example.scpmisystem.api

import retrofit2.http.*
import com.example.scpmisystem.model.*

interface ScpmiApi {

    @POST("register")
    suspend fun register(@Body request: AuthRequest): AuthResponse

    @POST("login")
    suspend fun login(@Body request: AuthRequest): AuthResponse

    // ✅ UPDATED: district added
    @GET("recommend-crop")
    suspend fun recommend(
        @Query("state") state: String,
        @Query("district") district: String,
        @Query("season") season: String
    ): RecommendResponse

    // ✅ FIXED: removed crop + city → now district flow
    @GET("mandi-prices")
    suspend fun markets(
        @Query("state") state: String,
        @Query("district") district: String,
        @Query("season") season: String
    ): MandiResponse

    // ✅ CORRECT (no change needed)
    @GET("production-analysis")
    suspend fun production(
        @Query("state") state: String
    ): ProductionResponse

    // ✅ UPDATED: district added
    @GET("ai-predict-yield")
    suspend fun predict(
        @Query("state") state: String,
        @Query("district") district: String,
        @Query("season") season: String,
        @Query("crop") crop: String,
        @Query("area") area: Double
    ): PredictResponse
}

