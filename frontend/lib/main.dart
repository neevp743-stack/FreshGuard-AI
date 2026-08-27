import 'package:flutter/material.dart';
import 'theme/app_theme.dart';
import 'screens/splash_screen.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';
import 'screens/main_navigation_screen.dart';
import 'screens/add_item_screen.dart';
import 'screens/barcode_scanner_screen.dart';
import 'screens/camera_ocr_screen.dart';
import 'screens/vision_scanner_screen.dart';
import 'screens/ai_assistant_screen.dart';
import 'screens/cook_first_screen.dart';
import 'screens/ai_insights_screen.dart';

void main() {
  runApp(const FreshGuardApp());
}

class FreshGuardApp extends StatelessWidget {
  const FreshGuardApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FreshGuard AI',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.dark, // Default to modern sleek dark mode
      initialRoute: '/splash',
      routes: {
        '/splash': (context) => const SplashScreen(),
        '/login': (context) => const LoginScreen(),
        '/register': (context) => const RegisterScreen(),
        '/home': (context) => const MainNavigationScreen(),
        '/add-item': (context) => const AddItemScreen(),
        '/barcode-scanner': (context) => const BarcodeScannerScreen(),
        '/camera-ocr': (context) => const CameraOCRScreen(),
        '/vision-scanner': (context) => const VisionScannerScreen(),
        '/ai-assistant': (context) => const AIAssistantScreen(),
        '/cook-first': (context) => const CookFirstScreen(),
        '/ai-insights': (context) => const AIInsightsScreen(),
      },
    );
  }
}
