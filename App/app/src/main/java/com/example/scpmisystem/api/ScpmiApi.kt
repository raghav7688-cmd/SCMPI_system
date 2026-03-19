package com.example.scpmisystem.api

import com.example.scpmisystem.model.*
import retrofit2.http.*

interface ScpmiApi {

    @POST("register")
    suspend fun register(@Body request: AuthRequest): AuthResponse

    @POST("login")
    suspend fun login(@Body request: AuthRequest): AuthResponse

    @GET("recommend-crop")
    suspend fun recommend(
        @Query("state") state: String,
        @Query("season") season: String
    ): RecommendResponse

    @GET("mandi-prices")
    suspend fun markets(
    @Query("crop") crop: String,
    @Query("city") city: String? = null  
    ): MarketsResponse

    @GET("production-analysis")
    suspend fun production(
        @Query("state") state: String
    ): ProductionResponse

    @GET("ai-predict-yield")
    suspend fun predict(
        @Query("state") state: String,
        @Query("season") season: String,
        @Query("crop") crop: String,
        @Query("area") area: Double
    ): PredictResponse
}