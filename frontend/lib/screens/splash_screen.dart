import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) {
        Navigator.pushReplacementNamed(context, '/login');
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: AppTheme.primaryGreen.withOpacity(0.15),
                shape: BoxShape.circle,
                border: Border.all(color: AppTheme.primaryGreen, width: 2),
              ),
              child: const Icon(
                Icons.shield_outlined,
                size: 72,
                color: AppTheme.primaryGreen,
              ),
            ),
            const SizedBox(height: 24),
            const Text(
              'FreshGuard AI',
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Colors.white,
                letterSpacing: 1.2,
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Know. Use. Refill. Waste Less.',
              style: TextStyle(
                fontSize: 14,
                color: AppTheme.darkTextSecondary,
                letterSpacing: 0.8,
              ),
            ),
            const SizedBox(height: 48),
            const CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(AppTheme.primaryGreen),
            ),
          ],
        ),
      ),
    );
  }
}
