import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../theme/app_theme.dart';
import '../services/api_service.dart';

class VisionScannerScreen extends StatefulWidget {
  const VisionScannerScreen({super.key});

  @override
  State<VisionScannerScreen> createState() => _VisionScannerScreenState();
}

class _VisionScannerScreenState extends State<VisionScannerScreen> {
  final ImagePicker _picker = ImagePicker();
  bool _isProcessing = false;
  Uint8List? _imageBytes;
  int _imageWidth = 640;
  int _imageHeight = 640;
  String _lifecycleState = "NOT_TRAINED";
  String _statusMessage = "";
  List<Map<String, dynamic>> _detections = [];
  Map<int, bool> _selectedDetections = {};
  Map<int, double> _quantityMap = {};

  @override
  void initState() {
    super.initState();
    _loadVisionStatus();
  }

  Future<void> _loadVisionStatus() async {
    final status = await ApiService.fetchVisionStatus();
    if (mounted) {
      setState(() {
        _lifecycleState = status['lifecycle_state'] ?? "NOT_TRAINED";
        _statusMessage = status['message'] ?? "";
      });
    }
  }

  Future<void> _captureOrPickImage(ImageSource source) async {
    try {
      final XFile? photo = await _picker.pickImage(
        source: source,
        maxWidth: 1600,
        maxHeight: 1600,
        imageQuality: 85,
      );

      if (photo == null) return;

      final bytes = await photo.readAsBytes();
      setState(() {
        _imageBytes = bytes;
        _isProcessing = true;
      });

      final res = await ApiService.detectVisionObjects(bytes, photo.name);

      if (mounted) {
        setState(() {
          _isProcessing = false;
          _imageWidth = res['image_width'] ?? 640;
          _imageHeight = res['image_height'] ?? 640;
          _lifecycleState = res['lifecycle_state'] ?? "NOT_TRAINED";
          _statusMessage = res['message'] ?? "";
          List rawList = res['detections'] ?? [];
          _detections = rawList.cast<Map<String, dynamic>>();

          _selectedDetections.clear();
          _quantityMap.clear();
          for (int i = 0; i < _detections.length; i++) {
            _selectedDetections[i] = true;
            _quantityMap[i] = 1.0;
          }
        });
      }
    } catch (_) {
      if (mounted) {
        setState(() => _isProcessing = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        title: const Text("Custom Vision AI Scanner"),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // Status Banner
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: _lifecycleState == "READY" ? AppTheme.primaryGreen.withOpacity(0.15) : Colors.amber.withOpacity(0.15),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: _lifecycleState == "READY" ? AppTheme.primaryGreen : Colors.amber),
              ),
              child: Row(
                children: [
                  Icon(
                    _lifecycleState == "READY" ? Icons.check_circle : Icons.info_outline,
                    color: _lifecycleState == "READY" ? AppTheme.primaryGreen : Colors.amber,
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      "State: $_lifecycleState • $_statusMessage",
                      style: TextStyle(color: _lifecycleState == "READY" ? AppTheme.primaryGreen : Colors.amber, fontSize: 12, fontWeight: FontWeight.bold),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Image Preview Container with CustomPainter Bounding Boxes
            if (_imageBytes != null)
              Container(
                height: 300,
                width: double.infinity,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppTheme.accentEmerald, width: 2),
                ),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(14),
                  child: Stack(
                    children: [
                      Positioned.fill(
                        child: Image.memory(_imageBytes!, fit: BoxFit.cover),
                      ),
                      Positioned.fill(
                        child: CustomPaint(
                          painter: BoundingBoxPainter(
                            detections: _detections,
                            imageWidth: _imageWidth,
                            imageHeight: _imageHeight,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              )
            else
              Container(
                height: 220,
                width: double.infinity,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppTheme.accentEmerald.withOpacity(0.5), width: 1.5),
                ),
                child: const Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.center_focus_strong, color: AppTheme.accentEmerald, size: 60),
                      SizedBox(height: 10),
                      Text("Capture or pick photo for multi-object detection", style: TextStyle(color: Colors.white70)),
                    ],
                  ),
                ),
              ),
            const SizedBox(height: 16),

            // Action Buttons
            if (_isProcessing)
              const CircularProgressIndicator(color: AppTheme.primaryGreen)
            else
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGreen, padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12)),
                    onPressed: () => _captureOrPickImage(ImageSource.camera),
                    icon: const Icon(Icons.camera_alt),
                    label: const Text("Take Photo"),
                  ),
                  const SizedBox(width: 12),
                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(backgroundColor: AppTheme.darkSurfaceVariant, padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12)),
                    onPressed: () => _captureOrPickImage(ImageSource.gallery),
                    icon: const Icon(Icons.photo_library),
                    label: const Text("Gallery Pick"),
                  ),
                ],
              ),
            const SizedBox(height: 20),

            // Detections Checklist Section
            if (_detections.isNotEmpty) ...[
              const Align(
                alignment: Alignment.centerLeft,
                child: Text("AI Detected Products Checklist", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
              ),
              const SizedBox(height: 10),
              ListView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: _detections.length,
                itemBuilder: (context, idx) {
                  final det = _detections[idx];
                  final String className = det['class_name'] ?? 'Object';
                  final double conf = (det['confidence'] as num?)?.toDouble() ?? 0.0;
                  final bool isLowConf = det['requires_confirmation'] ?? (conf < 0.50);
                  final bool isSelected = _selectedDetections[idx] ?? true;

                  return Card(
                    color: AppTheme.darkSurface,
                    margin: const EdgeInsets.only(bottom: 8),
                    child: ListTile(
                      leading: Checkbox(
                        activeColor: AppTheme.primaryGreen,
                        value: isSelected,
                        onChanged: (val) {
                          setState(() => _selectedDetections[idx] = val ?? false);
                        },
                      ),
                      title: Text(className.toUpperCase(), style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                      subtitle: Text(
                        isLowConf ? "⚠️ Low Confidence (${(conf * 100).toStringAsFixed(1)}%) - Verify" : "Confidence: ${(conf * 100).toStringAsFixed(1)}%",
                        style: TextStyle(color: isLowConf ? Colors.orange : AppTheme.darkTextSecondary, fontSize: 12),
                      ),
                      trailing: SizedBox(
                        width: 90,
                        child: Row(
                          children: [
                            IconButton(
                              icon: const Icon(Icons.remove_circle_outline, color: Colors.white70, size: 18),
                              onPressed: () {
                                setState(() {
                                  _quantityMap[idx] = max(0.5, (_quantityMap[idx] ?? 1.0) - 0.5);
                                });
                              },
                            ),
                            Text("${_quantityMap[idx] ?? 1.0}", style: const TextStyle(color: Colors.white, fontSize: 12)),
                          ],
                        ),
                      ),
                    ),
                  );
                },
              ),
              const SizedBox(height: 16),

              SizedBox(
                width: double.infinity,
                height: 48,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGreen, foregroundColor: Colors.white),
                  onPressed: () async {
                    for (int i = 0; i < _detections.length; i++) {
                      if (_selectedDetections[i] == true) {
                        final name = _detections[i]['class_name'] ?? 'Object';
                        final qty = _quantityMap[i] ?? 1.0;
                        await ApiService.addInventoryItem({
                          'product_name': name.toString().toUpperCase(),
                          'category': 'Produce',
                          'quantity': qty,
                          'unit': 'pcs',
                          'storage_location': 'Refrigerator',
                        });
                      }
                    }
                    if (mounted) {
                      Navigator.pushReplacementNamed(context, '/home');
                    }
                  },
                  child: const Text("Add Selected Items to Inventory", style: TextStyle(fontWeight: FontWeight.bold)),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  double max(double a, double b) => a > b ? a : b;
}

class BoundingBoxPainter extends CustomPainter {
  final List<Map<String, dynamic>> detections;
  final int imageWidth;
  final int imageHeight;

  BoundingBoxPainter({required this.detections, required this.imageWidth, required this.imageHeight});

  @override
  void paint(Canvas canvas, Size size) {
    if (imageWidth == 0 || imageHeight == 0) return;

    final paint = Paint()
      ..color = AppTheme.primaryGreen
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3.0;

    final scaleX = size.width / imageWidth;
    final scaleY = size.height / imageHeight;

    for (final det in detections) {
      final bbox = det['bounding_box'] as Map<String, dynamic>?;
      if (bbox == null) continue;

      final x1 = (bbox['x1'] as num).toDouble() * scaleX;
      final y1 = (bbox['y1'] as num).toDouble() * scaleY;
      final x2 = (bbox['x2'] as num).toDouble() * scaleX;
      final y2 = (bbox['y2'] as num).toDouble() * scaleY;

      final rect = Rect.fromLTRB(x1, y1, x2, y2);
      canvas.drawRect(rect, paint);
    }
  }

  @override
  bool shouldRepaint(covariant BoundingBoxPainter oldDelegate) => true;
}
