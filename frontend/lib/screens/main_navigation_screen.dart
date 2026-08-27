import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'home_dashboard_screen.dart';
import 'inventory_screen.dart';
import 'add_item_screen.dart';
import 'smart_cart_screen.dart';
import 'profile_screen.dart';

class MainNavigationScreen extends StatefulWidget {
  const MainNavigationScreen({super.key});

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    HomeDashboardScreen(),
    InventoryScreen(),
    AddItemScreen(),
    SmartCartScreen(),
    ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      drawer: Drawer(
        backgroundColor: AppTheme.darkSurface,
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            UserAccountsDrawerHeader(
              decoration: const BoxDecoration(color: AppTheme.primaryDarkGreen),
              accountName: const Text("Alex Morgan", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              accountEmail: const Text("demo@freshguard.ai", style: TextStyle(color: Colors.white70)),
              currentAccountPicture: CircleAvatar(
                backgroundColor: AppTheme.accentEmerald,
                child: const Text("AM", style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.restaurant_menu, color: AppTheme.primaryGreen),
              title: const Text("Cook-First (Use Soon)", style: TextStyle(color: Colors.white)),
              onTap: () {
                Navigator.pop(context);
                Navigator.pushNamed(context, '/cook-first');
              },
            ),
            ListTile(
              leading: const Icon(Icons.smart_toy_outlined, color: AppTheme.accentEmerald),
              title: const Text("AI Assistant Chat", style: TextStyle(color: Colors.white)),
              onTap: () {
                Navigator.pop(context);
                Navigator.pushNamed(context, '/ai-assistant');
              },
            ),
            ListTile(
              leading: const Icon(Icons.analytics_outlined, color: Colors.blueAccent),
              title: const Text("AI Waste Analytics", style: TextStyle(color: Colors.white)),
              onTap: () {
                Navigator.pop(context);
                Navigator.pushNamed(context, '/ai-insights');
              },
            ),
            const Divider(color: Colors.white24),
            ListTile(
              leading: const Icon(Icons.camera_alt_outlined, color: AppTheme.statusExpiring),
              title: const Text("Package OCR Scanner", style: TextStyle(color: Colors.white)),
              onTap: () {
                Navigator.pop(context);
                Navigator.pushNamed(context, '/camera-ocr');
              },
            ),
            ListTile(
              leading: const Icon(Icons.qr_code_scanner, color: AppTheme.statusHealthy),
              title: const Text("Barcode Scanner", style: TextStyle(color: Colors.white)),
              onTap: () {
                Navigator.pop(context);
                Navigator.pushNamed(context, '/barcode-scanner');
              },
            ),
            const Divider(color: Colors.white24),
            ListTile(
              leading: const Icon(Icons.logout, color: Colors.redAccent),
              title: const Text("Sign Out", style: TextStyle(color: Colors.redAccent)),
              onTap: () => Navigator.pushReplacementNamed(context, '/login'),
            ),
          ],
        ),
      ),
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (index) => setState(() => _currentIndex = index),
        backgroundColor: AppTheme.darkSurface,
        indicatorColor: AppTheme.primaryGreen.withOpacity(0.3),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home, color: AppTheme.primaryGreen), label: "Home"),
          NavigationDestination(icon: Icon(Icons.kitchen_outlined), selectedIcon: Icon(Icons.kitchen, color: AppTheme.primaryGreen), label: "Inventory"),
          NavigationDestination(icon: Icon(Icons.add_circle_outline), selectedIcon: Icon(Icons.add_circle, color: AppTheme.primaryGreen), label: "Add"),
          NavigationDestination(icon: Icon(Icons.shopping_cart_outlined), selectedIcon: Icon(Icons.shopping_cart, color: AppTheme.primaryGreen), label: "Smart Cart"),
          NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person, color: AppTheme.primaryGreen), label: "Profile"),
        ],
      ),
    );
  }
}
