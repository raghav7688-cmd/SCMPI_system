package com.example.scpmisystem

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable

@Composable
fun AppNavigation(navController: NavHostController) {
    NavHost(
        navController = navController,
        startDestination = "login"
    ) {
        composable("login") {
            LoginScreen(
                onLoginClick = { username, password ->
                    // Handle login logic here
                    // For now, just navigate to home
                    navController.navigate("home") {
                        popUpTo("login") { inclusive = true }
                    }
                },
                onNavigateToRegister = {
                    navController.navigate("register")
                }
            )
        }

        composable("register") {
            RegisterScreen(
                onRegisterClick = { username, password ->
                    // Handle registration logic here
                    // User will be navigated back to login in RegisterScreen
                },
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }

        composable("home") {
            HomeScreen(modifier = androidx.compose.ui.Modifier)
        }
    }
}

