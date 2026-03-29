package com.example.scpmisystem

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ExitToApp
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.scpmisystem.api.RetrofitInstance
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(onLogout: () -> Unit) {

    var selectedTab by remember { mutableStateOf(0) }
    val tabs = listOf("Recommend", "Mandi", "Production", "Predict")

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("SCPMI Dashboard") },
                actions = {
                    IconButton(onClick = onLogout) {
                        Icon(Icons.AutoMirrored.Filled.ExitToApp, "Logout")
                    }
                }
            )
        }
    ) { padding ->

        Column(modifier = Modifier.padding(padding)) {

            TabRow(selectedTabIndex = selectedTab) {
                tabs.forEachIndexed { index, title ->
                    Tab(
                        selected = selectedTab == index,
                        onClick = { selectedTab = index },
                        text = { Text(title) }
                    )
                }
            }

            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(16.dp)
            ) {
                when (selectedTab) {
                    0 -> RecommendCropTab()
                    1 -> MarketPricesTab()
                    2 -> ProductionAnalysisTab()
                    3 -> PredictYieldTab()
                }
            }
        }
    }
}

@Composable
fun InputField(value: String, label: String, onChange: (String) -> Unit) {
    OutlinedTextField(
        value = value,
        onValueChange = onChange,
        label = { Text(label) },
        modifier = Modifier
            .fillMaxWidth()
            .padding(bottom = 12.dp),
        singleLine = true
    )
}

@Composable
fun ResultCard(result: String) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 16.dp)
    ) {
        Text(
            text = result,
            modifier = Modifier.padding(16.dp)
        )
    }
}

@Composable
fun ErrorText(msg: String) {
    Text(
        text = msg,
        color = MaterialTheme.colorScheme.error,
        fontSize = 12.sp,
        modifier = Modifier.padding(top = 10.dp)
    )
}

@Composable
fun RecommendCropTab() {
    var state by remember { mutableStateOf("") }
    var district by remember { mutableStateOf("") }
    var season by remember { mutableStateOf("") }

    var result by remember { mutableStateOf("") }
    var error by remember { mutableStateOf("") }
    var loading by remember { mutableStateOf(false) }

    val scope = rememberCoroutineScope()

    Column(Modifier.verticalScroll(rememberScrollState())) {

        Text("Crop Recommendation", style = MaterialTheme.typography.titleLarge)

        InputField(state, "State") { state = it }
        InputField(district, "District") { district = it }
        InputField(season, "Season") { season = it }

        Button(
            onClick = {
                if (state.isBlank() || district.isBlank() || season.isBlank()) {
                    error = "Fill all fields"
                    return@Button
                }

                scope.launch {
                    loading = true
                    error = ""
                    try {
                        val res = RetrofitInstance.api.recommend(state, district, season)
                        result = "🌱 ${res.crop}\n💰 ₹${res.estimated_price}\n📍 ${res.district}\n📊 ${res.reason}"
                    } catch (e: Exception) {
                        error = e.message ?: "Error"
                    }
                    loading = false
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            if (loading) CircularProgressIndicator() else Text("Get Recommendation")
        }

        if (error.isNotEmpty()) ErrorText(error)
        if (result.isNotEmpty()) ResultCard(result)
    }
}

@Composable
fun MarketPricesTab() {
    var state by remember { mutableStateOf("") }
    var district by remember { mutableStateOf("") }
    var season by remember { mutableStateOf("") }

    var result by remember { mutableStateOf("") }
    var error by remember { mutableStateOf("") }
    var loading by remember { mutableStateOf(false) }

    val scope = rememberCoroutineScope()

    Column(Modifier.verticalScroll(rememberScrollState())) {

        Text("Market Prices", style = MaterialTheme.typography.titleLarge)

        InputField(state, "State") { state = it }
        InputField(district, "District") { district = it }
        InputField(season, "Season") { season = it }

        Button(onClick = {
            scope.launch {
                loading = true
                error = ""
                try {
                    val res = RetrofitInstance.api.markets(state, district, season)
                    result = "🌾 ${res.crop}\n💰 ₹${res.estimated_price ?: "N/A"}\n📍 ${res.district}\n🗓️ ${res.latest_price_column ?: "No recent price column"}"
                } catch (e: Exception) {
                    error = e.message ?: ""
                }
                loading = false
            }
        }, modifier = Modifier.fillMaxWidth()) {
            if (loading) CircularProgressIndicator() else Text("Get Prices")
        }

        if (error.isNotEmpty()) ErrorText(error)
        if (result.isNotEmpty()) ResultCard(result)
    }
}

@Composable
fun ProductionAnalysisTab() {
    var state by remember { mutableStateOf("") }
    var result by remember { mutableStateOf("") }
    var loading by remember { mutableStateOf(false) }

    val scope = rememberCoroutineScope()

    Column {

        Text("Production Analysis", style = MaterialTheme.typography.titleLarge)

        InputField(state, "State") { state = it }

        Button(onClick = {
            scope.launch {
                loading = true
                runCatching {
                    RetrofitInstance.api.production(state)
                }.onSuccess { res ->
                    result = "📊 Production: ${res.production ?: "N/A"}\n🛒 Demand: ${res.demand ?: "N/A"}\n📉 Gap: ${res.demand_gap ?: "N/A"}\n📈 ${res.status}"
                }
                loading = false
            }
        }, modifier = Modifier.fillMaxWidth()) {
            if (loading) CircularProgressIndicator() else Text("Analyze")
        }

        if (result.isNotEmpty()) ResultCard(result)
    }
}

@Composable
fun PredictYieldTab() {
    var state by remember { mutableStateOf("") }
    var district by remember { mutableStateOf("") }
    var season by remember { mutableStateOf("") }
    var crop by remember { mutableStateOf("") }
    var area by remember { mutableStateOf("") }

    var result by remember { mutableStateOf("") }
    var error by remember { mutableStateOf("") }

    val scope = rememberCoroutineScope()

    Column(Modifier.verticalScroll(rememberScrollState())) {

        Text("Yield Prediction", style = MaterialTheme.typography.titleLarge)

        InputField(state, "State") { state = it }
        InputField(district, "District") { district = it }
        InputField(season, "Season") { season = it }
        InputField(crop, "Crop") { crop = it }
        InputField(area, "Area") { area = it }

        Button(onClick = {
            val areaVal = area.toDoubleOrNull()
            if (areaVal == null) {
                error = "Invalid area"
                return@Button
            }

            scope.launch {
                runCatching {
                    RetrofitInstance.api.predict(state, district, season, crop, areaVal)
                }.onSuccess { res ->
                    result = "🌾 ${res.crop}\n📊 Yield: ${res.predicted_yield}\n🎯 Confidence: ${res.confidence}"
                    error = ""
                }.onFailure { e ->
                    error = e.message ?: "Error"
                }
            }
        }, modifier = Modifier.fillMaxWidth()) {
            Text("Predict")
        }

        if (error.isNotEmpty()) ErrorText(error)
        if (result.isNotEmpty()) ResultCard(result)
    }
}
