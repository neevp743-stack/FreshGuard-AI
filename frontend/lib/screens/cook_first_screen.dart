import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class CookFirstScreen extends StatelessWidget {
  const CookFirstScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final useFirstItems = [
      {"name": "Amul Taaza Toned Milk", "qty": "0.5 L", "expiry": "Expires tomorrow", "icon": Icons.local_drink, "color": AppTheme.statusExpiring},
      {"name": "Fresh Red Tomatoes", "qty": "4 pcs", "expiry": "Expires in 2 days", "icon": Icons.eco, "color": AppTheme.statusExpiring},
      {"name": "Britannia Whole Wheat Bread", "qty": "1 pack", "expiry": "Expires in 2 days", "icon": Icons.bakery_dining, "color": AppTheme.statusExpiring},
      {"name": "Organic Bananas", "qty": "6 pcs", "expiry": "Expires in 3 days", "icon": Icons.shopping_bag, "color": AppTheme.statusHealthy},
    ];

    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      appBar: AppBar(
        title: Row(
          children: const [
            Icon(Icons.restaurant_menu, color: AppTheme.primaryGreen),
            SizedBox(width: 8),
            Text("Cook-First (Use Soon)"),
          ],
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppTheme.primaryDarkGreen.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppTheme.primaryGreen),
                ),
                child: Row(
                  children: const [
                    Icon(Icons.eco_outlined, color: AppTheme.primaryGreen, size: 32),
                    SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        "FreshGuard AI identifies products that must be consumed soon to help your household eliminate food waste.",
                        style: TextStyle(color: Colors.white, fontSize: 13, height: 1.4),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              const Text("USE FIRST ITEMS 🥛🍅🍞", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
              const SizedBox(height: 12),

              ListView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: useFirstItems.length,
                itemBuilder: (context, index) {
                  final item = useFirstItems[index];
                  final Color col = item["color"] as Color;
                  return Card(
                    margin: const EdgeInsets.only(bottom: 12),
                    child: ListTile(
                      contentPadding: const EdgeInsets.all(12),
                      leading: CircleAvatar(
                        backgroundColor: col.withOpacity(0.2),
                        child: Icon(item["icon"] as IconData, color: col),
                      ),
                      title: Text(item["name"] as String, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 16)),
                      subtitle: Text(item["expiry"] as String, style: TextStyle(color: col, fontWeight: FontWeight.w600)),
                      trailing: Text(item["qty"] as String, style: const TextStyle(color: Colors.white70, fontWeight: FontWeight.bold)),
                    ),
                  );
                },
              ),
              const SizedBox(height: 20),

              // AI Suggested Recipe
              const Text("AI Recipe Suggestion 👨‍🍳", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppTheme.darkSurface,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text("Creamy Tomato Toast & Warm Milk", style: TextStyle(color: AppTheme.accentEmerald, fontWeight: FontWeight.bold, fontSize: 16)),
                    SizedBox(height: 8),
                    Text(
                      "Uses: Milk (0.5L), Tomatoes (4 pcs), Whole Wheat Bread.\nPreparation time: 10 mins.\nThis recipe utilizes 3 items expiring within 48 hours!",
                      style: TextStyle(color: AppTheme.darkTextSecondary, fontSize: 13, height: 1.4),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
