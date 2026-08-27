import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../models/models.dart';
import '../services/api_service.dart';

class HomeDashboardScreen extends StatefulWidget {
  const HomeDashboardScreen({super.key});

  @override
  State<HomeDashboardScreen> createState() => _HomeDashboardScreenState();
}

class _HomeDashboardScreenState extends State<HomeDashboardScreen> {
  bool _isLoading = true;
  AIInsightSummaryModel? _insights;
  List<InventoryItem> _expiringItems = [];
  List<InventoryItem> _runningLowItems = [];

  @override
  void initState() {
    super.initState();
    _loadDashboardData();
  }

  Future<void> _loadDashboardData() async {
    setState(() => _isLoading = true);
    try {
      final insights = await ApiService.fetchAIInsights();
      final inventory = await ApiService.fetchInventory();

      final expiring = inventory.where((i) => i.status == 'Expiring Soon').toList();
      final low = inventory.where((i) => i.status == 'Running Low').toList();

      if (mounted) {
        setState(() {
          _insights = insights;
          _expiringItems = expiring.isNotEmpty ? expiring : _getMockExpiring();
          _runningLowItems = low.isNotEmpty ? low : _getMockRunningLow();
          _isLoading = false;
        });
      }
    } catch (_) {
      if (mounted) {
        setState(() {
          _insights = AIInsightSummaryModel(
            healthyCount: 18,
            expiringSoonCount: 4,
            expiredCount: 2,
            runningLowCount: 3,
            foodWasteEstimate: 12.50,
            topConsumedCategory: 'Dairy',
            recentInsightMessage: 'You usually consume 1 litre of milk every 2 days. Based on your current stock, you may need milk tomorrow.'
          );
          _expiringItems = _getMockExpiring();
          _runningLowItems = _getMockRunningLow();
          _isLoading = false;
        });
      }
    }
  }

  List<InventoryItem> _getMockExpiring() {
    final now = DateTime.now();
    return [
      InventoryItem(id: 1, productName: 'Amul Taaza Toned Milk', category: 'Dairy', quantity: 0.5, unit: 'L', storageLocation: 'Fridge', expiryDate: now.add(const Duration(days: 1)), status: 'Expiring Soon', daysUntilExpiry: 1),
      InventoryItem(id: 2, productName: 'Britannia Wheat Bread', category: 'Bakery', quantity: 1.0, unit: 'pack', storageLocation: 'Pantry', expiryDate: now.add(const Duration(days: 2)), status: 'Expiring Soon', daysUntilExpiry: 2),
      InventoryItem(id: 3, productName: 'Fresh Red Tomatoes', category: 'Vegetables', quantity: 4.0, unit: 'pcs', storageLocation: 'Fridge', expiryDate: now.add(const Duration(days: 2)), status: 'Expiring Soon', daysUntilExpiry: 2),
    ];
  }

  List<InventoryItem> _getMockRunningLow() {
    return [
      InventoryItem(id: 1, productName: 'Amul Taaza Toned Milk', category: 'Dairy', quantity: 0.5, unit: 'L', storageLocation: 'Fridge', status: 'Running Low'),
      InventoryItem(id: 4, productName: 'Fresh Red Apples', category: 'Fruits', quantity: 2.0, unit: 'pcs', storageLocation: 'Pantry', status: 'Running Low'),
      InventoryItem(id: 5, productName: 'Organic Eggs', category: 'Eggs', quantity: 3.0, unit: 'pcs', storageLocation: 'Fridge', status: 'Running Low'),
    ];
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator(color: AppTheme.primaryGreen));
    }

    final summary = _insights ?? AIInsightSummaryModel(
      healthyCount: 18, expiringSoonCount: 4, expiredCount: 2, runningLowCount: 3,
      foodWasteEstimate: 12.50, topConsumedCategory: 'Dairy',
      recentInsightMessage: 'You usually consume 1 litre of milk every 2 days. Based on your current stock, you may need milk tomorrow.'
    );

    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: _loadDashboardData,
          color: AppTheme.primaryGreen,
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: const [
                        Text("Good Morning 👋", style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white)),
                        SizedBox(height: 4),
                        Text("Morgan Family Kitchen", style: TextStyle(color: AppTheme.darkTextSecondary, fontSize: 14)),
                      ],
                    ),
                    IconButton(
                      icon: const Icon(Icons.notifications_outlined, color: Colors.white),
                      onPressed: () {},
                    ),
                  ],
                ),
                const SizedBox(height: 20),

                // Kitchen Status Banner
                const Text("Your Kitchen Status", style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: Colors.white)),
                const SizedBox(height: 12),
                GridView.count(
                  crossAxisCount: 2,
                  shrinkWrap: true,
                  crossAxisSpacing: 10,
                  mainAxisSpacing: 10,
                  childAspectRatio: 2.2,
                  physics: const NeverScrollableScrollPhysics(),
                  children: [
                    _buildStatusCard("Healthy", "${summary.healthyCount} Items", AppTheme.statusHealthy, Icons.check_circle_outline),
                    _buildStatusCard("Expiring Soon", "${summary.expiringSoonCount} Items", AppTheme.statusExpiring, Icons.timer_outlined),
                    _buildStatusCard("Expired", "${summary.expiredCount} Items", AppTheme.statusExpired, Icons.warning_amber_rounded),
                    _buildStatusCard("Running Low", "${summary.runningLowCount} Items", AppTheme.statusRunningLow, Icons.shopping_basket_outlined),
                  ],
                ),
                const SizedBox(height: 20),

                // Quick Action Buttons
                Row(
                  children: [
                    Expanded(
                      child: ElevatedButton.icon(
                        onPressed: () => Navigator.pushNamed(context, '/add-item'),
                        icon: const Icon(Icons.add, size: 18),
                        label: const Text("Add Item"),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppTheme.primaryGreen,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 12),
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: ElevatedButton.icon(
                        onPressed: () => Navigator.pushNamed(context, '/camera-ocr'),
                        icon: const Icon(Icons.camera_alt_outlined, size: 18),
                        label: const Text("Scan Product"),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppTheme.darkSurfaceVariant,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 12),
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: ElevatedButton.icon(
                        onPressed: () => Navigator.pushNamed(context, '/home'),
                        icon: const Icon(Icons.shopping_cart_outlined, size: 18),
                        label: const Text("Smart Cart"),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppTheme.accentEmerald.withOpacity(0.2),
                          foregroundColor: AppTheme.accentEmerald,
                          padding: const EdgeInsets.symmetric(vertical: 12),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 24),

                // AI Insight Card
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [AppTheme.primaryDarkGreen, AppTheme.darkSurface],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: AppTheme.primaryGreen.withOpacity(0.4)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: const [
                          Icon(Icons.auto_awesome, color: AppTheme.accentEmerald, size: 20),
                          SizedBox(width: 8),
                          Text("AI Insight", style: TextStyle(fontWeight: FontWeight.bold, color: AppTheme.accentEmerald, fontSize: 15)),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Text(
                        summary.recentInsightMessage,
                        style: const TextStyle(color: Colors.white, fontSize: 14, height: 1.4),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 24),

                // Expiring Soon Section
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: const [
                    Text("Expiring Soon ⏰", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
                    Text("See All", style: TextStyle(color: AppTheme.primaryGreen, fontWeight: FontWeight.w600)),
                  ],
                ),
                const SizedBox(height: 12),
                ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: _expiringItems.length,
                  itemBuilder: (context, index) {
                    final item = _expiringItems[index];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: AppTheme.statusExpiring.withOpacity(0.2),
                          child: const Icon(Icons.timer, color: AppTheme.statusExpiring),
                        ),
                        title: Text(item.productName, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                        subtitle: Text("Expires in ${item.daysUntilExpiry ?? 1} day(s)", style: const TextStyle(color: AppTheme.statusExpiring)),
                        trailing: Text("${item.quantity} ${item.unit}", style: const TextStyle(color: Colors.white70, fontWeight: FontWeight.w600)),
                      ),
                    );
                  },
                ),
                const SizedBox(height: 20),

                // Running Low Section
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: const [
                    Text("Running Low 🛒", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
                    Text("See All", style: TextStyle(color: AppTheme.primaryGreen, fontWeight: FontWeight.w600)),
                  ],
                ),
                const SizedBox(height: 12),
                ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: _runningLowItems.length,
                  itemBuilder: (context, index) {
                    final item = _runningLowItems[index];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: AppTheme.statusRunningLow.withOpacity(0.2),
                          child: const Icon(Icons.shopping_bag, color: AppTheme.statusRunningLow),
                        ),
                        title: Text(item.productName, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                        subtitle: const Text("Estimated 1 day remaining", style: TextStyle(color: AppTheme.statusRunningLow)),
                        trailing: Text("${item.quantity} ${item.unit}", style: const TextStyle(color: Colors.white70, fontWeight: FontWeight.w600)),
                      ),
                    );
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildStatusCard(String title, String subtitle, Color color, IconData icon) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: AppTheme.darkSurface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Row(
        children: [
          Icon(icon, color: color, size: 24),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(title, style: TextStyle(color: color, fontSize: 13, fontWeight: FontWeight.bold)),
                Text(subtitle, style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w500)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
