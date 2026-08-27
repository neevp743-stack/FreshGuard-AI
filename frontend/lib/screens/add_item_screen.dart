import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../services/api_service.dart';

class AddItemScreen extends StatefulWidget {
  const AddItemScreen({super.key});

  @override
  State<AddItemScreen> createState() => _AddItemScreenState();
}

class _AddItemScreenState extends State<AddItemScreen> {
  final _nameController = TextEditingController();
  final _brandController = TextEditingController();
  final _quantityController = TextEditingController(text: "1.0");
  String _selectedUnit = "pcs";
  String _selectedCategory = "Dairy";
  String _selectedLocation = "Refrigerator";
  DateTime? _expiryDate;
  bool _isLoading = false;

  final List<String> _categories = ["Dairy", "Fruits", "Vegetables", "Bakery", "Meat", "Eggs", "Beverages", "Snacks", "Grains", "Spices", "Frozen", "Other"];
  final List<String> _locations = ["Refrigerator", "Freezer", "Pantry", "Kitchen Shelf", "Other"];

  Future<void> _saveProduct() async {
    if (_nameController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Product name is required")));
      return;
    }

    setState(() => _isLoading = true);
    try {
      await ApiService.addInventoryItem({
        'product_name': _nameController.text.trim(),
        'brand': _brandController.text.trim(),
        'category': _selectedCategory,
        'quantity': double.tryParse(_quantityController.text) ?? 1.0,
        'unit': _selectedUnit,
        'storage_location': _selectedLocation,
        'expiry_date': _expiryDate?.toIso8601String(),
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Product saved to inventory!")));
        Navigator.pushReplacementNamed(context, '/home');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: ${e.toString()}")));
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      appBar: AppBar(title: const Text("Add New Product")),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Quick Scan Option Banners
            Row(
              children: [
                Expanded(
                  child: InkWell(
                    onTap: () => Navigator.pushNamed(context, '/barcode-scanner'),
                    child: Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: AppTheme.darkSurface,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: AppTheme.primaryGreen.withOpacity(0.5)),
                      ),
                      child: Column(
                        children: const [
                          Icon(Icons.qr_code_scanner, color: AppTheme.primaryGreen, size: 32),
                          SizedBox(height: 8),
                          Text("Scan Barcode", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13)),
                        ],
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: InkWell(
                    onTap: () => Navigator.pushNamed(context, '/camera-ocr'),
                    child: Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: AppTheme.darkSurface,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: AppTheme.accentEmerald.withOpacity(0.5)),
                      ),
                      child: Column(
                        children: const [
                          Icon(Icons.camera_alt_outlined, color: AppTheme.accentEmerald, size: 32),
                          SizedBox(height: 8),
                          Text("AI Package OCR", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13)),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),

            const Text("Or Manual Entry", style: TextStyle(color: AppTheme.darkTextSecondary, fontWeight: FontWeight.bold, fontSize: 16)),
            const SizedBox(height: 16),

            TextField(
              controller: _nameController,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                labelText: "Product Name *",
                labelStyle: const TextStyle(color: AppTheme.darkTextSecondary),
                filled: true,
                fillColor: AppTheme.darkSurface,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
              ),
            ),
            const SizedBox(height: 12),

            TextField(
              controller: _brandController,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                labelText: "Brand (Optional)",
                labelStyle: const TextStyle(color: AppTheme.darkTextSecondary),
                filled: true,
                fillColor: AppTheme.darkSurface,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
              ),
            ),
            const SizedBox(height: 12),

            Row(
              children: [
                Expanded(
                  flex: 2,
                  child: TextField(
                    controller: _quantityController,
                    keyboardType: TextInputType.number,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      labelText: "Quantity",
                      labelStyle: const TextStyle(color: AppTheme.darkTextSecondary),
                      filled: true,
                      fillColor: AppTheme.darkSurface,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  flex: 1,
                  child: DropdownButtonFormField<String>(
                    value: _selectedUnit,
                    dropdownColor: AppTheme.darkSurface,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      filled: true,
                      fillColor: AppTheme.darkSurface,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                    ),
                    items: ["pcs", "L", "ml", "kg", "g", "pack"].map((u) => DropdownMenuItem(value: u, child: Text(u))).toList(),
                    onChanged: (val) => setState(() => _selectedUnit = val!),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),

            DropdownButtonFormField<String>(
              value: _selectedCategory,
              dropdownColor: AppTheme.darkSurface,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                labelText: "Category",
                labelStyle: const TextStyle(color: AppTheme.darkTextSecondary),
                filled: true,
                fillColor: AppTheme.darkSurface,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
              ),
              items: _categories.map((c) => DropdownMenuItem(value: c, child: Text(c))).toList(),
              onChanged: (val) => setState(() => _selectedCategory = val!),
            ),
            const SizedBox(height: 12),

            DropdownButtonFormField<String>(
              value: _selectedLocation,
              dropdownColor: AppTheme.darkSurface,
              style: const TextStyle(color: Colors.white),
              decoration: InputDecoration(
                labelText: "Storage Location",
                labelStyle: const TextStyle(color: AppTheme.darkTextSecondary),
                filled: true,
                fillColor: AppTheme.darkSurface,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
              ),
              items: _locations.map((l) => DropdownMenuItem(value: l, child: Text(l))).toList(),
              onChanged: (val) => setState(() => _selectedLocation = val!),
            ),
            const SizedBox(height: 12),

            // Expiry Date Picker
            ListTile(
              tileColor: AppTheme.darkSurface,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              title: Text(
                _expiryDate == null ? "Select Expiry Date" : "Expiry: ${_expiryDate!.day}/${_expiryDate!.month}/${_expiryDate!.year}",
                style: const TextStyle(color: Colors.white),
              ),
              trailing: const Icon(Icons.calendar_today, color: AppTheme.primaryGreen),
              onTap: () async {
                final date = await showDatePicker(
                  context: context,
                  initialDate: DateTime.now().add(const Duration(days: 7)),
                  firstDate: DateTime.now(),
                  lastDate: DateTime.now().add(const Duration(days: 730)),
                );
                if (date != null) {
                  setState(() => _expiryDate = date);
                }
              },
            ),
            const SizedBox(height: 24),

            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _saveProduct,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.primaryGreen,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text("Save Product", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
