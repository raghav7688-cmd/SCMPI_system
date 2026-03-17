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

    val scope = rememberCoroutineScope()

    Column(modifier = modifier.padding(16.dp)) {

        TextField(value = state, onValueChange = {state = it}, label={Text("State")})

        TextField(value = season, onValueChange = {season = it}, label={Text("Season")})

        TextField(value = crop, onValueChange = {crop = it}, label={Text("Crop")})

        TextField(value = area, onValueChange = {area = it}, label={Text("Area")})

        Spacer(modifier = Modifier.height(16.dp))

        Button(onClick = {
            scope.launch {
                try {
                    val areaValue = area.toDoubleOrNull()
                    if (areaValue != null) {
                        val response = RetrofitInstance.api.predict(
                            state,
                            season,
                            crop,
                            areaValue
                        )
                        println("Predicted yield: ${response.predicted_yield}")
                    } else {
                        println("Please enter a valid area value")
                    }
                } catch (e: Exception) {
                    println("Error: ${e.message}")
                }
            }

        }) {

            Text("Predict Yield")

        }

    }

}