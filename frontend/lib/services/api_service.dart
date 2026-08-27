import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/models.dart';

class ApiService {
  static const String baseUrl = "http://127.0.0.1:8000/api";
  static String? _authToken;

  static void setAuthToken(String token) {
    _authToken = token;
  }

  static Map<String, String> get _headers {
    final Map<String, String> headers = {
      'Content-Type': 'application/json',
    };
    if (_authToken != null) {
      headers['Authorization'] = 'Bearer $_authToken';
    }
    return headers;
  }

  // Auth Endpoints
  static Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse("$baseUrl/auth/login"),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      _authToken = data['access_token'];
      return data;
    } else {
      throw Exception(jsonDecode(response.body)['detail'] ?? 'Login failed');
    }
  }

  static Future<Map<String, dynamic>> register(String email, String password, String fullName, String householdName) async {
    final response = await http.post(
      Uri.parse("$baseUrl/auth/register"),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'password': password,
        'full_name': fullName,
        'household_name': householdName
      }),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      _authToken = data['access_token'];
      return data;
    } else {
      throw Exception(jsonDecode(response.body)['detail'] ?? 'Registration failed');
    }
  }

  // Inventory Endpoints
  static Future<List<InventoryItem>> fetchInventory({String? location, String? category, String? status, String? search}) async {
    try {
      final Uri uri = Uri.parse("$baseUrl/inventory").replace(queryParameters: {
        if (location != null && location != 'All') 'location': location,
        if (category != null && category != 'All') 'category': category,
        if (status != null && status != 'All') 'status': status,
        if (search != null && search.isNotEmpty) 'search': search,
      });
      final response = await http.get(uri, headers: _headers);
      if (response.statusCode == 200) {
        List list = jsonDecode(response.body);
        return list.map((i) => InventoryItem.fromJson(i)).toList();
      }
    } catch (_) {}
    return [];
  }

  static Future<InventoryItem> addInventoryItem(Map<String, dynamic> itemData) async {
    final response = await http.post(
      Uri.parse("$baseUrl/inventory"),
      headers: _headers,
      body: jsonEncode(itemData),
    );
    if (response.statusCode == 200) {
      return InventoryItem.fromJson(jsonDecode(response.body));
    }
    throw Exception("Failed to save product");
  }

  static Future<void> deleteInventoryItem(int id) async {
    await http.delete(Uri.parse("$baseUrl/inventory/$id"), headers: _headers);
  }

  static Future<void> logConsumption(int id, double quantity, String logType) async {
    await http.post(
      Uri.parse("$baseUrl/inventory/$id/log-consumption"),
      headers: _headers,
      body: jsonEncode({'quantity_consumed': quantity, 'log_type': logType}),
    );
  }

  // Scanner & OCR Endpoints
  static Future<BarcodeResult> lookupBarcode(String barcode) async {
    final response = await http.post(
      Uri.parse("$baseUrl/scanner/barcode"),
      headers: _headers,
      body: jsonEncode({'barcode': barcode}),
    );
    if (response.statusCode == 200) {
      return BarcodeResult.fromJson(jsonDecode(response.body));
    }
    return BarcodeResult(found: false, barcode: barcode);
  }

  static Future<OCRResult> scanOCRText(String rawText) async {
    final response = await http.post(
      Uri.parse("$baseUrl/scanner/ocr"),
      headers: _headers,
      body: jsonEncode({'raw_text': rawText}),
    );
    if (response.statusCode == 200) {
      return OCRResult.fromJson(jsonDecode(response.body));
    }
    return OCRResult(detected: false, confidenceScore: 0.0);
  }

  static Future<OCRResult> scanOCRImage(List<int> imageBytes, String filename) async {
    try {
      final request = http.MultipartRequest("POST", Uri.parse("$baseUrl/scanner/ocr/image"));
      if (_authToken != null) {
        request.headers['Authorization'] = 'Bearer $_authToken';
      }
      request.files.add(http.MultipartFile.fromBytes(
        'file',
        imageBytes,
        filename: filename,
      ));
      final streamed = await request.send();
      final response = await http.Response.fromStream(streamed);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return OCRResult(
          detected: data['success'] ?? false,
          productName: data['product_name'],
          brand: data['brand'],
          expiryDate: data['expiry_date'],
          mfgDate: data['manufacturing_date'],
          quantity: (data['quantity'] as num?)?.toDouble() ?? 1.0,
          unit: data['unit'] ?? 'pcs',
          batchNumber: data['batch_number'],
          confidenceScore: (data['confidence'] as num?)?.toDouble() != null ? (data['confidence'] as num).toDouble() * 100 : 85.0,
        );
      }
    } catch (_) {}
    return OCRResult(detected: false, confidenceScore: 0.0);
  }

  // Vision AI & Multi-Modal Scanner Endpoints
  static Future<Map<String, dynamic>> fetchVisionStatus() async {
    try {
      final response = await http.get(Uri.parse("$baseUrl/scanner/vision/status"), headers: _headers);
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (_) {}
    return {
      "lifecycle_state": "NOT_TRAINED",
      "model_available": false,
      "model_version": "0.1.0",
      "classes_count": 15,
      "confidence_threshold": 0.50,
      "message": "Vision model integration is ready; training is pending the real grocery dataset."
    };
  }

  static Future<Map<String, dynamic>> detectVisionObjects(List<int> imageBytes, String filename) async {
    try {
      final request = http.MultipartRequest("POST", Uri.parse("$baseUrl/scanner/vision/detect"));
      if (_authToken != null) {
        request.headers['Authorization'] = 'Bearer $_authToken';
      }
      request.files.add(http.MultipartFile.fromBytes(
        'file',
        imageBytes,
        filename: filename,
      ));
      final streamed = await request.send();
      final response = await http.Response.fromStream(streamed);
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (_) {}
    return {
      "success": false,
      "lifecycle_state": "NOT_TRAINED",
      "detections": [],
      "message": "Vision model integration is ready; training is pending the real grocery dataset."
    };
  }

  static Future<void> sendVisionFeedback(String predictedClass, double confidence, String correctedClass, {bool optInImageRetention = false}) async {
    try {
      await http.post(
        Uri.parse("$baseUrl/scanner/vision/feedback"),
        headers: _headers,
        body: jsonEncode({
          'predicted_class': predictedClass,
          'confidence': confidence,
          'corrected_class': correctedClass,
          'opt_in_image_retention': optInImageRetention
        }),
      );
    } catch (_) {}
  }

  // Device Token Registration Endpoint
  static Future<void> registerDeviceToken(String token, {String platform = "android"}) async {
    try {
      await http.post(
        Uri.parse("$baseUrl/notifications/device-token"),
        headers: _headers,
        body: jsonEncode({'token': token, 'platform': platform}),
      );
    } catch (_) {}
  }

  // AI Endpoints
  static Future<AIInsightSummaryModel> fetchAIInsights() async {
    final response = await http.get(Uri.parse("$baseUrl/ai/insights"), headers: _headers);
    if (response.statusCode == 200) {
      return AIInsightSummaryModel.fromJson(jsonDecode(response.body));
    }
    return AIInsightSummaryModel(
      healthyCount: 18, expiringSoonCount: 4, expiredCount: 2, runningLowCount: 3,
      foodWasteEstimate: 12.50, topConsumedCategory: 'Dairy', recentInsightMessage: 'You consume milk fast.'
    );
  }

  static Future<List<RecommendationItem>> fetchRecommendations() async {
    final response = await http.get(Uri.parse("$baseUrl/ai/recommendations"), headers: _headers);
    if (response.statusCode == 200) {
      List list = jsonDecode(response.body);
      return list.map((i) => RecommendationItem.fromJson(i)).toList();
    }
    return [];
  }

  static Future<String> askAIAssistant(String query) async {
    final response = await http.post(
      Uri.parse("$baseUrl/ai/assistant"),
      headers: _headers,
      body: jsonEncode({'query': query}),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body)['answer'];
    }
    return "Could not connect to AI Assistant.";
  }

  // Cart Endpoints
  static Future<SmartCartModel> fetchCart() async {
    final response = await http.get(Uri.parse("$baseUrl/cart"), headers: _headers);
    if (response.statusCode == 200) {
      return SmartCartModel.fromJson(jsonDecode(response.body));
    }
    return SmartCartModel(id: 1, householdId: 1, totalEstimatedPrice: 0.0, status: 'active', items: []);
  }

  static Future<void> addCartItem(String productName, double quantity, String unit, double price, String reason) async {
    await http.post(
      Uri.parse("$baseUrl/cart/items"),
      headers: _headers,
      body: jsonEncode({
        'product_name': productName,
        'quantity': quantity,
        'unit': unit,
        'estimated_price': price,
        'reason': reason
      }),
    );
  }

  static Future<Map<String, dynamic>> confirmOrder() async {
    final response = await http.post(Uri.parse("$baseUrl/cart/confirm"), headers: _headers);
    return jsonDecode(response.body);
  }

  // Notification Endpoints
  static Future<List<NotificationItem>> fetchNotifications() async {
    final response = await http.get(Uri.parse("$baseUrl/notifications"), headers: _headers);
    if (response.statusCode == 200) {
      List list = jsonDecode(response.body);
      return list.map((i) => NotificationItem.fromJson(i)).toList();
    }
    return [];
  }
}
