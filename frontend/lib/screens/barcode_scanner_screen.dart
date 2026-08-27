import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import '../theme/app_theme.dart';
import '../models/models.dart';
import '../services/api_service.dart';

class BarcodeScannerScreen extends StatefulWidget {
  const BarcodeScannerScreen({super.key});

  @override
  State<BarcodeScannerScreen> createState() => _BarcodeScannerScreenState();
}

class _BarcodeScannerScreenState extends State<BarcodeScannerScreen> {
  final MobileScannerController _scannerController = MobileScannerController(
    formats: [
      BarcodeFormat.ean13,
      BarcodeFormat.ean8,
      BarcodeFormat.upcA,
      BarcodeFormat.upcE,
      BarcodeFormat.code128,
      BarcodeFormat.qrCode,
    ],
  );

  bool _isProcessing = false;
  String? _lastScannedCode;
  DateTime? _lastScanTime;

  final _quantityController = TextEditingController(text: "1.0");
  String _selectedLocation = "Refrigerator";
  DateTime? _expiryDate = DateTime.now().add(const Duration(days: 7));

  @override
  void dispose() {
    _scannerController.dispose();
    super.dispose();
  }

  void _onBarcodeDetected(BarcodeCapture capture) {
    if (_isProcessing) return;

    final List<Barcode> barcodes = capture.barcodes;
    if (barcodes.isEmpty) return;

    final String? code = barcodes.first.rawValue;
    if (code == null || code.trim().isEmpty) return;

    // Prevent Duplicate Scans within 3 seconds
    final now = DateTime.now();
    if (_lastScannedCode == code && _lastScanTime != null && now.difference(_lastScanTime!).inSeconds < 3) {
      return;
    }

    _lastScannedCode = code;
    _lastScanTime = now;
    _handleBarcodeLookup(code.trim());
  }

  Future<void> _handleBarcodeLookup(String barcode) async {
    setState(() => _isProcessing = true);
    try {
      final res = await ApiService.lookupBarcode(barcode);
      if (mounted) {
        setState(() => _isProcessing = false);
        _showConfirmationModal(res);
      }
    } catch (_) {
      if (mounted) {
        setState(() => _isProcessing = false);
      }
    }
  }

  void _showConfirmationModal(BarcodeResult res) {
    if (!res.found) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          backgroundColor: AppTheme.darkSurface,
          title: const Text("Product Not Found", style: TextStyle(color: Colors.white)),
          content: Text("No product matches barcode '${res.barcode}'. Would you like to enter details manually?", style: const TextStyle(color: AppTheme.darkTextSecondary)),
          actions: [
            TextButton(onPressed: () => Navigator.pop(context), child: const Text("Cancel")),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGreen),
              onPressed: () {
                Navigator.pop(context);
                Navigator.pushReplacementNamed(context, '/add-item');
              },
              child: const Text("Enter Manually"),
            ),
          ],
        ),
      );
      return;
    }

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: AppTheme.darkSurface,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) {
        return Padding(
          padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom + 20, left: 20, right: 20, top: 20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Icon(Icons.check_circle, color: AppTheme.statusHealthy, size: 28),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(res.productName ?? "Scanned Product", style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
                  ),
                ],
              ),
              const SizedBox(height: 4),
              Text("Brand: ${res.brand ?? 'Generic'} • Category: ${res.category ?? 'Other'}", style: const TextStyle(color: AppTheme.darkTextSecondary)),
              const Divider(height: 24, color: Colors.white24),

              TextField(
                controller: _quantityController,
                keyboardType: TextInputType.number,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: "Quantity (${res.defaultUnit ?? 'pcs'})",
                  labelStyle: const TextStyle(color: AppTheme.darkTextSecondary),
                  filled: true,
                  fillColor: AppTheme.darkBackground,
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                ),
              ),
              const SizedBox(height: 12),

              DropdownButtonFormField<String>(
                value: _selectedLocation,
                dropdownColor: AppTheme.darkBackground,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: "Storage Location",
                  labelStyle: const TextStyle(color: AppTheme.darkTextSecondary),
                  filled: true,
                  fillColor: AppTheme.darkBackground,
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                ),
                items: ["Refrigerator", "Freezer", "Pantry", "Kitchen Shelf", "Other"].map((l) => DropdownMenuItem(value: l, child: Text(l))).toList(),
                onChanged: (val) => setState(() => _selectedLocation = val!),
              ),
              const SizedBox(height: 12),

              ListTile(
                tileColor: AppTheme.darkBackground,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                title: Text(_expiryDate == null ? "Select Expiry Date" : "Expiry: ${_expiryDate!.day}/${_expiryDate!.month}/${_expiryDate!.year}", style: const TextStyle(color: Colors.white)),
                trailing: const Icon(Icons.calendar_today, color: AppTheme.primaryGreen),
                onTap: () async {
                  final date = await showDatePicker(
                    context: context,
                    initialDate: DateTime.now().add(const Duration(days: 7)),
                    firstDate: DateTime.now(),
                    lastDate: DateTime.now().add(const Duration(days: 730)),
                  );
                  if (date != null) setState(() => _expiryDate = date);
                },
              ),
              const SizedBox(height: 20),

              SizedBox(
                width: double.infinity,
                height: 48,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGreen, foregroundColor: Colors.white),
                  onPressed: () async {
                    await ApiService.addInventoryItem({
                      'product_name': res.productName,
                      'brand': res.brand,
                      'category': res.category ?? 'Other',
                      'quantity': double.tryParse(_quantityController.text) ?? 1.0,
                      'unit': res.defaultUnit ?? 'pcs',
                      'storage_location': _selectedLocation,
                      'expiry_date': _expiryDate?.toIso8601String(),
                      'barcode': res.barcode,
                    });
                    if (mounted) {
                      Navigator.pop(context);
                      Navigator.pushReplacementNamed(context, '/home');
                    }
                  },
                  child: const Text("Confirm & Add to Inventory", style: TextStyle(fontWeight: FontWeight.bold)),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        title: const Text("Real Barcode Scanner"),
        actions: [
          IconButton(
            icon: const Icon(Icons.flash_on, color: Colors.amber),
            onPressed: () => _scannerController.toggleTorch(),
          ),
        ],
      ),
      body: Stack(
        children: [
          // Real Mobile Scanner Hardware Camera Stream
          MobileScanner(
            controller: _scannerController,
            onDetect: _onBarcodeDetected,
          ),

          // Scanner Overlay Bounding Frame
          Center(
            child: Container(
              width: 280,
              height: 180,
              decoration: BoxDecoration(
                border: Border.all(color: AppTheme.primaryGreen, width: 3),
                borderRadius: BorderRadius.circular(16),
              ),
              child: const Center(
                child: Divider(color: AppTheme.primaryGreen, thickness: 2),
              ),
            ),
          ),

          // Fallback barcode trigger shortcuts for desktop/web testing
          Positioned(
            bottom: 24,
            left: 16,
            right: 16,
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(color: Colors.black87, borderRadius: BorderRadius.circular(12)),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text("Hardware Camera Active (EAN-13, UPC, Code 128)", style: TextStyle(color: Colors.white70, fontSize: 12)),
                  const SizedBox(height: 8),
                  Wrap(
                    alignment: WrapAlignment.center,
                    spacing: 8,
                    children: [
                      _mockBarcodeButton("Amul Milk", "8901058000147"),
                      _mockBarcodeButton("Bread", "8901262010056"),
                      _mockBarcodeButton("Eggs", "8901725111234"),
                    ],
                  ),
                ],
              ),
            ),
          ),

          if (_isProcessing)
            const Center(child: CircularProgressIndicator(color: AppTheme.primaryGreen)),
        ],
      ),
    );
  }

  Widget _mockBarcodeButton(String label, String code) {
    return ElevatedButton.icon(
      style: ElevatedButton.styleFrom(backgroundColor: AppTheme.darkSurface),
      onPressed: () => _handleBarcodeLookup(code),
      icon: const Icon(Icons.qr_code, color: AppTheme.accentEmerald, size: 14),
      label: Text(label, style: const TextStyle(fontSize: 11, color: Colors.white)),
    );
  }
}
