import 'package:flutter/material.dart';

class AppTheme {
  // Brand Colors
  static const Color primaryGreen = Color(0xFF10B981);
  static const Color primaryDarkGreen = Color(0xFF047857);
  static const Color accentEmerald = Color(0xFF34D399);

  // Kitchen Status Indicator Colors
  static const Color statusHealthy = Color(0xFF10B981);
  static const Color statusExpiring = Color(0xFFF59E0B);
  static const Color statusExpired = Color(0xFFEF4444);
  static const Color statusRunningLow = Color(0xFF6366F1);

  // Dark Theme Palette
  static const Color darkBackground = Color(0xFF0F172A);
  static const Color darkSurface = Color(0xFF1E293B);
  static const Color darkSurfaceVariant = Color(0xFF334155);
  static const Color darkTextPrimary = Color(0xFFF8FAFC);
  static const Color darkTextSecondary = Color(0xFF94A3B8);

  // Light Theme Palette
  static const Color lightBackground = Color(0xFFF8FAFC);
  static const Color lightSurface = Color(0xFFFFFFFF);
  static const Color lightSurfaceVariant = Color(0xFFF1F5F9);
  static const Color lightTextPrimary = Color(0xFF0F172A);
  static const Color lightTextSecondary = Color(0xFF64748B);

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: darkBackground,
      colorScheme: ColorScheme.dark(
        primary: primaryGreen,
        secondary: accentEmerald,
        surface: darkSurface,
        background: darkBackground,
        error: statusExpired,
      ),
      cardTheme: CardTheme(
        color: darkSurface,
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: darkBackground,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: TextStyle(
          color: darkTextPrimary,
          fontSize: 20,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      scaffoldBackgroundColor: lightBackground,
      colorScheme: ColorScheme.light(
        primary: primaryGreen,
        secondary: primaryDarkGreen,
        surface: lightSurface,
        background: lightBackground,
        error: statusExpired,
      ),
      cardTheme: CardTheme(
        color: lightSurface,
        elevation: 2,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: lightBackground,
        elevation: 0,
        centerTitle: false,
        titleTextStyle: TextStyle(
          color: lightTextPrimary,
          fontSize: 20,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}
