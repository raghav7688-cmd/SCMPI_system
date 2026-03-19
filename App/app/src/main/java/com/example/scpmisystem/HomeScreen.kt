package com.example.scpmisystem

import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.foundation.layout.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.scpmisystem.api.RetrofitInstance
import kotlinx.coroutines.launch

@Composable
fun HomeScreen(modifier: Modifier = Modifier) {

    var state by remember { mutableStateOf("") }
    var season by remember { mutableStateOf("") }
    var crop by remember { mutableStateOf("") }
    var area by remember { mutableStateOf("") }
    var result by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }

    val scope = rememberCoroutineScope()

    Column(modifier = modifier.padding(16.dp)) {

        TextField(value = state, onValueChange = {state = it}, label={Text("State")})

        TextField(value = season, onValueChange = {season = it}, label={Text("Season")})

        TextField(value = crop, onValueChange = {crop = it}, label={Text("Crop")})

        TextField(value = area, onValueChange = {area = it}, label={Text("Area")})

        Spacer(modifier = Modifier.height(16.dp))

        Button(onClick = {
            scope.launch {
                isLoading = true
                result = ""
                try {
                    val areaValue = area.toDoubleOrNull()
                    if (areaValue != null) {
                        val response = RetrofitInstance.api.predict(
                            state,
                            season,
                            crop,
                            areaValue
                        )
                        result = "Predicted yield: ${response.predicted_yield}, Confidence: ${response.confidence}"
                    } else {
                        result = "Please enter a valid area value"
                    }
                } catch (e: Exception) {
                    result = "Error: ${e.message}"
                } finally {
                    isLoading = false
                }
            }
        }, enabled = !isLoading) {
            if (isLoading) {
                CircularProgressIndicator(modifier = Modifier.size(24.dp))
            } else {
                Text("Predict Yield")
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        if (result.isNotEmpty()) {
            Text(text = result)
        }

    }

}