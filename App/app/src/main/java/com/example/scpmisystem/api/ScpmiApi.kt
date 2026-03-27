package com.example.scpmisystem.api

import com.example.scpmisystem.model.AuthRequest
import com.example.scpmisystem.model.AuthResponse
import com.example.scpmisystem.model.MandiResponse
import com.example.scpmisystem.model.PredictResponse
import com.example.scpmisystem.model.ProductionResponse
import com.example.scpmisystem.model.RecommendResponse
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query

interface ScpmiApi {

    @POST("register")
    suspend fun register(@Body request: AuthRequest): AuthResponse

    @POST("login")
    suspend fun login(@Body request: AuthRequest): AuthResponse

    @GET("recommend-crop")
    suspend fun recommend(
        @Query("state") state: String,
        @Query("district") district: String,
        @Query("season") season: String
    ): RecommendResponse

    @GET("mandi-prices")
    suspend fun markets(
        @Query("state") state: String,
        @Query("district") district: String,
        @Query("season") season: String
    ): MandiResponse

    @GET("production-analysis")
    suspend fun production(
        @Query("state") state: String
    ): ProductionResponse

    @GET("ai-predict-yield")
    suspend fun predict(
        @Query("state") state: String,
        @Query("district") district: String,
        @Query("season") season: String,
        @Query("crop") crop: String,
        @Query("area") area: Double
    ): PredictResponse
}

