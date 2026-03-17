package com.example.scpmisystem.api

import com.example.scpmisystem.model.MarketsResponse
import com.example.scpmisystem.model.PredictResponse
import com.example.scpmisystem.model.ProductionResponse
import com.example.scpmisystem.model.RecommendResponse
import retrofit2.http.GET
import retrofit2.http.Query

interface ScpmiApi {

    @GET("recommend-crop")
    suspend fun recommend(
        @Query("state") state: String,
        @Query("season") season: String
    ): RecommendResponse

    @GET("mandi-prices")
    suspend fun markets(
        @Query("crop") crop: String
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