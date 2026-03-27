package com.example.scpmisystem

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.*

/**
 * 🔹 All routes in one place (avoid hardcoded strings)
 */
sealed class Screen(val route: String) {
    object Login : Screen("login")
    object Register : Screen("register")
    object Home : Screen("home")
    object Recommend : Screen("recommend")
    object Mandi : Screen("mandi")
    object Production : Screen("production")
    object Predict : Screen("predict")
}

@Composable
fun AppNavigation(
    navController: NavHostController = rememberNavController()
) {

    NavHost(
        navController = navController,
        startDestination = Screen.Login.route
    ) {

        /**
         * 🔹 LOGIN SCREEN
         */
        composable(Screen.Login.route) {
            LoginScreen(
                onLoginSuccess = {
                    navController.navigate(Screen.Home.route) {
                        popUpTo(Screen.Login.route) { inclusive = true }
                    }
                },
                onNavigateToRegister = {
                    navController.navigate(Screen.Register.route)
                }
            )
        }

        /**
         * 🔹 REGISTER SCREEN
         */
        composable(Screen.Register.route) {
            RegisterScreen(
                onRegisterSuccess = {
                    navController.navigate(Screen.Home.route) {
                        popUpTo(Screen.Login.route) { inclusive = true }
                    }
                },
                onNavigateBack = {
                    navController.popBackStack()
                }
            )
        }

        /**
         * 🔹 HOME SCREEN
         */
        composable(Screen.Home.route) {
            HomeScreen(
                onLogout = {
                    navController.navigate(Screen.Login.route) {
                        popUpTo(Screen.Home.route) { inclusive = true }
                    }
                }
            )
        }

        /**
         * 🔹 FEATURE SCREENS
         */
        composable(Screen.Recommend.route) {
            RecommendCropTab()
        }

        composable(Screen.Mandi.route) {
            MarketPricesTab()
        }

        composable(Screen.Production.route) {
            ProductionAnalysisTab()
        }

        composable(Screen.Predict.route) {
            PredictYieldTab()
        }
    }
}