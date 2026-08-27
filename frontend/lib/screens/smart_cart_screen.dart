import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../models/models.dart';
import '../services/api_service.dart';

class SmartCartScreen extends StatefulWidget {
  const SmartCartScreen({super.key});

  @override
  State<SmartCartScreen> createState() => _SmartCartScreenState();
}

class _SmartCartScreenState extends State<SmartCartScreen> {
  bool _isLoading = true;
  SmartCartModel? _cart;

  @override
  void initState() {
    super.initState();
    _loadCart();
  }

  Future<void> _loadCart() async {
    setState(() => _isLoading = true);
    try {
      final cart = await ApiService.fetchCart();
      if (mounted) {
        setState(() {
          _cart = cart.items.isNotEmpty ? cart : _getMockCart();
          _isLoading = false;
        });
      }
    } catch (_) {
      if (mounted) {
        setState(() {
          _cart = _getMockCart();
          _isLoading = false;
        });
      }
    }
  }

  SmartCartModel _getMockCart() {
    return SmartCartModel(
      id: 1,
      householdId: 1,
      totalEstimatedPrice: 184.0,
      status: 'active',
      items: [
        CartItemModel(id: 1, productName: 'Amul Taaza Toned Milk 1L', quantity: 1.0, unit: 'L', estimatedPrice: 64.0, reason: 'Running low (1 day remaining)', priority: 'Urgent', confirmed: false),
        CartItemModel(id: 2, productName: 'Britannia Whole Wheat Bread', quantity: 1.0, unit: 'pack', estimatedPrice: 45.0, reason: 'Weekly purchase pattern', priority: 'Normal', confirmed: false),
        CartItemModel(id: 3, productName: 'Fresh Red Apples 1kg', quantity: 1.0, unit: 'kg', estimatedPrice: 75.0, reason: 'Predicted shortage', priority: 'Normal', confirmed: false),
      ],
    );
  }

  Future<void> _confirmCartOrder() async {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: AppTheme.darkSurface,
        title: const Text("Confirm Grocery Order", style: TextStyle(color: Colors.white)),
        content: Text("Proceed with user-approved refill for estimated total ₹${_cart?.totalEstimatedPrice.toStringAsFixed(0)}?", style: const TextStyle(color: AppTheme.darkTextSecondary)),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text("Cancel")),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGreen),
            onPressed: () async {
              Navigator.pop(context);
              try {
                await ApiService.confirmOrder();
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text("Order confirmed successfully! Items moved to purchase logs.")),
                  );
                  _loadCart();
                }
              } catch (_) {
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text("Mock Order Confirmed! (Explicit user approval recorded)")),
                  );
                }
              }
            },
            child: const Text("Approve Order"),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        backgroundColor: AppTheme.darkBackground,
        body: Center(child: CircularProgressIndicator(color: AppTheme.primaryGreen)),
      );
    }

    final cart = _cart ?? _getMockCart();

    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      appBar: AppBar(
        title: const Text("Smart Grocery Cart"),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _loadCart),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Smart Banner
            Container(
              margin: const EdgeInsets.all(16),
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: AppTheme.primaryGreen.withOpacity(0.15),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.primaryGreen.withOpacity(0.4)),
              ),
              child: Row(
                children: const [
                  Icon(Icons.shield, color: AppTheme.primaryGreen, size: 24),
                  SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      "Explicit Approval Required: FreshGuard AI will never place paid orders without your confirmation.",
                      style: TextStyle(color: Colors.white70, fontSize: 12),
                    ),
                  ),
                ],
              ),
            ),

            // Cart Items
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                itemCount: cart.items.length,
                itemBuilder: (context, index) {
                  final item = cart.items[index];
                  return Card(
                    margin: const EdgeInsets.only(bottom: 12),
                    child: ListTile(
                      contentPadding: const EdgeInsets.all(12),
                      title: Text(item.productName, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 16)),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const SizedBox(height: 4),
                          Text("Reason: ${item.reason ?? 'AI Recommendation'}", style: const TextStyle(color: AppTheme.accentEmerald, fontSize: 13)),
                          const SizedBox(height: 4),
                          Text("${item.quantity} ${item.unit} • Est. ₹${item.estimatedPrice.toStringAsFixed(0)}", style: const TextStyle(color: AppTheme.darkTextSecondary, fontSize: 13)),
                        ],
                      ),
                      trailing: IconButton(
                        icon: const Icon(Icons.delete_outline, color: Colors.redAccent),
                        onPressed: () {
                          setState(() {
                            cart.items.removeAt(index);
                          });
                        },
                      ),
                    ),
                  );
                },
              ),
            ),

            // Bottom Order Summary Bar
            Container(
              padding: const EdgeInsets.all(20),
              decoration: const BoxDecoration(
                color: AppTheme.darkSurface,
                borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
              ),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text("Estimated Total:", style: TextStyle(fontSize: 18, color: Colors.white, fontWeight: FontWeight.w600)),
                      Text("₹${cart.totalEstimatedPrice.toStringAsFixed(0)}", style: const TextStyle(fontSize: 22, color: AppTheme.primaryGreen, fontWeight: FontWeight.bold)),
                    ],
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    height: 52,
                    child: ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppTheme.primaryGreen,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      onPressed: cart.items.isEmpty ? null : _confirmCartOrder,
                      icon: const Icon(Icons.check_circle_outline),
                      label: const Text("Review & Approve Order", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
