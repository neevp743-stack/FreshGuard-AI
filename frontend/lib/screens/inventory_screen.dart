import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../models/models.dart';
import '../services/api_service.dart';

class InventoryScreen extends StatefulWidget {
  const InventoryScreen({super.key});

  @override
  State<InventoryScreen> createState() => _InventoryScreenState();
}

class _InventoryScreenState extends State<InventoryScreen> {
  String _selectedLocation = 'All';
  String _selectedCategory = 'All';
  String _searchQuery = '';
  bool _isLoading = true;
  List<InventoryItem> _items = [];

  final List<String> _locations = ['All', 'Refrigerator', 'Freezer', 'Pantry', 'Kitchen Shelf', 'Other'];
  final List<String> _categories = ['All', 'Dairy', 'Fruits', 'Vegetables', 'Bakery', 'Eggs', 'Grains', 'Other'];

  @override
  void initState() {
    super.initState();
    _loadInventory();
  }

  Future<void> _loadInventory() async {
    setState(() => _isLoading = true);
    try {
      final data = await ApiService.fetchInventory(
        location: _selectedLocation,
        category: _selectedCategory,
        search: _searchQuery,
      );
      if (mounted) {
        setState(() {
          _items = data.isNotEmpty ? data : _getMockInventory();
          _isLoading = false;
        });
      }
    } catch (_) {
      if (mounted) {
        setState(() {
          _items = _getMockInventory();
          _isLoading = false;
        });
      }
    }
  }

  List<InventoryItem> _getMockInventory() {
    final now = DateTime.now();
    return [
      InventoryItem(id: 1, productName: 'Amul Taaza Toned Milk', category: 'Dairy', quantity: 0.5, unit: 'L', storageLocation: 'Refrigerator', expiryDate: now.add(const Duration(days: 1)), status: 'Expiring Soon', daysUntilExpiry: 1),
      InventoryItem(id: 2, productName: 'Britannia Whole Wheat Bread', category: 'Bakery', quantity: 1.0, unit: 'pack', storageLocation: 'Pantry', expiryDate: now.add(const Duration(days: 2)), status: 'Expiring Soon', daysUntilExpiry: 2),
      InventoryItem(id: 3, productName: 'Fresh Red Apples 1kg', category: 'Fruits', quantity: 2.0, unit: 'pcs', storageLocation: 'Pantry', expiryDate: now.add(const Duration(days: 5)), status: 'Healthy', daysUntilExpiry: 5),
      InventoryItem(id: 4, productName: 'Organic Eggs 6 Pack', category: 'Eggs', quantity: 3.0, unit: 'pcs', storageLocation: 'Refrigerator', expiryDate: now.add(const Duration(days: 8)), status: 'Healthy', daysUntilExpiry: 8),
      InventoryItem(id: 5, productName: 'Greek Natural Yogurt', category: 'Dairy', quantity: 1.0, unit: 'cup', storageLocation: 'Refrigerator', expiryDate: now.subtract(const Duration(days: 1)), status: 'Expired', daysUntilExpiry: -1),
    ];
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'Healthy':
        return AppTheme.statusHealthy;
      case 'Expiring Soon':
        return AppTheme.statusExpiring;
      case 'Expired':
        return AppTheme.statusExpired;
      case 'Running Low':
        return AppTheme.statusRunningLow;
      default:
        return AppTheme.primaryGreen;
    }
  }

  void _showConsumptionModal(InventoryItem item) {
    showModalBottomSheet(
      context: context,
      backgroundColor: AppTheme.darkSurface,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) {
        return Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(item.productName, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
              const SizedBox(height: 8),
              Text("Current Stock: ${item.quantity} ${item.unit}", style: const TextStyle(color: AppTheme.darkTextSecondary)),
              const SizedBox(height: 20),
              const Text("Action:", style: TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _actionChip("Consume 1 Unit", Icons.restaurant, AppTheme.primaryGreen, () async {
                    await ApiService.logConsumption(item.id, 1.0, 'consumed');
                    Navigator.pop(context);
                    _loadInventory();
                  }),
                  _actionChip("Wasted / Expired", Icons.delete_outline, AppTheme.statusExpired, () async {
                    await ApiService.logConsumption(item.id, item.quantity, 'wasted');
                    Navigator.pop(context);
                    _loadInventory();
                  }),
                  _actionChip("Donated", Icons.volunteer_activism, Colors.amber, () async {
                    await ApiService.logConsumption(item.id, item.quantity, 'donated');
                    Navigator.pop(context);
                    _loadInventory();
                  }),
                ],
              ),
              const SizedBox(height: 16),
            ],
          ),
        );
      },
    );
  }

  Widget _actionChip(String label, IconData icon, Color color, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      child: Column(
        children: [
          CircleAvatar(radius: 26, backgroundColor: color.withOpacity(0.2), child: Icon(icon, color: color)),
          const SizedBox(height: 6),
          Text(label, style: TextStyle(color: color, fontSize: 12, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      appBar: AppBar(
        title: const Text("My Kitchen Inventory"),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _loadInventory),
        ],
      ),
      body: Column(
        children: [
          // Search Bar
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
            child: TextField(
              onChanged: (val) {
                _searchQuery = val;
                _loadInventory();
              },
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                hintText: "Search products...",
                hintStyle: const TextStyle(color: AppTheme.darkTextSecondary),
                prefixIcon: const Icon(Icons.search, color: AppTheme.primaryGreen),
                filled: true,
                fillColor: AppTheme.darkSurface,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
              ),
            ),
          ),

          // Location Filter Tabs
          SizedBox(
            height: 40,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 12),
              itemCount: _locations.length,
              itemBuilder: (context, index) {
                final loc = _locations[index];
                final isSelected = _selectedLocation == loc;
                return Padding(
                  padding: const EdgeInsets.only(right: 8.0),
                  child: FilterChip(
                    label: Text(loc),
                    selected: isSelected,
                    onSelected: (selected) {
                      setState(() => _selectedLocation = loc);
                      _loadInventory();
                    },
                    selectedColor: AppTheme.primaryGreen,
                    backgroundColor: AppTheme.darkSurface,
                    labelStyle: TextStyle(color: isSelected ? Colors.white : AppTheme.darkTextSecondary, fontWeight: FontWeight.w600),
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 8),

          // Item Count & List View
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator(color: AppTheme.primaryGreen))
                : _items.isEmpty
                    ? const Center(child: Text("No products found in this location", style: TextStyle(color: AppTheme.darkTextSecondary)))
                    : ListView.builder(
                        padding: const EdgeInsets.all(16),
                        itemCount: _items.length,
                        itemBuilder: (context, index) {
                          final item = _items[index];
                          final color = _getStatusColor(item.status);
                          return Card(
                            margin: const EdgeInsets.only(bottom: 12),
                            child: ListTile(
                              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                              leading: Container(
                                padding: const EdgeInsets.all(10),
                                decoration: BoxDecoration(
                                  color: color.withOpacity(0.15),
                                  shape: BoxShape.circle,
                                ),
                                child: Icon(
                                  item.category == 'Dairy' ? Icons.local_drink : item.category == 'Bakery' ? Icons.bakery_dining : Icons.shopping_bag,
                                  color: color,
                                ),
                              ),
                              title: Text(item.productName, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 16)),
                              subtitle: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const SizedBox(height: 4),
                                  Text("Location: ${item.storageLocation} • ${item.quantity} ${item.unit}", style: const TextStyle(color: AppTheme.darkTextSecondary, fontSize: 13)),
                                  const SizedBox(height: 4),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                    decoration: BoxDecoration(color: color.withOpacity(0.2), borderRadius: BorderRadius.circular(6)),
                                    child: Text(item.status, style: TextStyle(color: color, fontSize: 11, fontWeight: FontWeight.bold)),
                                  ),
                                ],
                              ),
                              trailing: IconButton(
                                icon: const Icon(Icons.more_vert, color: Colors.white70),
                                onPressed: () => _showConsumptionModal(item),
                              ),
                            ),
                          );
                        },
                      ),
          ),
        ],
      ),
    );
  }
}
