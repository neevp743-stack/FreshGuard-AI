import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class AIInsightsScreen extends StatelessWidget {
  const AIInsightsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      appBar: AppBar(
        title: Row(
          children: const [
            Icon(Icons.analytics_outlined, color: Colors.blueAccent),
            SizedBox(width: 8),
            Text("AI Insights & Waste Analytics"),
          ],
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Summary Cards Grid
              GridView.count(
                crossAxisCount: 2,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                childAspectRatio: 1.5,
                children: [
                  _metricCard("Food Waste Est.", "₹125.00", "Saved ₹185 this month", Icons.delete_outline, AppTheme.statusExpired),
                  _metricCard("Top Consumed", "Dairy (42%)", "Milk & Yogurt", Icons.local_drink, AppTheme.primaryGreen),
                  _metricCard("Grocery Cycle", "2.3 Days", "Average refill frequency", Icons.update, AppTheme.accentEmerald),
                  _metricCard("Waste Reduction", "-35%", "Compared to last month", Icons.trending_down, Colors.blueAccent),
                ],
              ),
              const SizedBox(height: 24),

              // AI Insight Note
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppTheme.darkSurface,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppTheme.primaryGreen.withOpacity(0.3)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text("AI Recommendation 💡", style: TextStyle(fontWeight: FontWeight.bold, color: AppTheme.primaryGreen, fontSize: 16)),
                    SizedBox(height: 8),
                    Text(
                      "\"You frequently purchase more bread than you consume before expiry. Try purchasing smaller half-loaf portions or storing excess slices in the freezer.\"",
                      style: TextStyle(color: Colors.white, fontSize: 13, height: 1.4),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              const Text("Category Spend Distribution", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
              const SizedBox(height: 12),
              _categoryBar("Dairy & Eggs", 0.45, AppTheme.primaryGreen),
              _categoryBar("Fruits & Veggies", 0.30, AppTheme.accentEmerald),
              _categoryBar("Bakery & Grains", 0.15, Colors.amber),
              _categoryBar("Beverages & Snacks", 0.10, Colors.blueAccent),
            ],
          ),
        ),
      ),
    );
  }

  Widget _metricCard(String title, String value, String sub, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppTheme.darkSurface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 20),
              const SizedBox(width: 6),
              Expanded(child: Text(title, style: const TextStyle(color: AppTheme.darkTextSecondary, fontSize: 12), overflow: TextOverflow.ellipsis)),
            ],
          ),
          const SizedBox(height: 6),
          Text(value, style: TextStyle(color: color, fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 2),
          Text(sub, style: const TextStyle(color: Colors.white54, fontSize: 10)),
        ],
      ),
    );
  }

  Widget _categoryBar(String category, double percent, Color color) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(category, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w500)),
              Text("${(percent * 100).toInt()}%", style: TextStyle(color: color, fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 6),
          LinearProgressIndicator(
            value: percent,
            color: color,
            backgroundColor: AppTheme.darkSurface,
            minHeight: 8,
            borderRadius: BorderRadius.circular(4),
          ),
        ],
      ),
    );
  }
}
