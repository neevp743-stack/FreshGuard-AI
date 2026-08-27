class UserProfile {
  final int userId;
  final String email;
  final String fullName;
  final int householdId;
  final String householdName;

  UserProfile({
    required this.userId,
    required this.email,
    required this.fullName,
    required this.householdId,
    required this.householdName,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      userId: json['user_id'] ?? 0,
      email: json['email'] ?? '',
      fullName: json['full_name'] ?? 'User',
      householdId: json['household_id'] ?? 1,
      householdName: json['household_name'] ?? 'My Kitchen',
    );
  }
}

class InventoryItem {
  final int id;
  final String productName;
  final String category;
  final String? brand;
  final double quantity;
  final String unit;
  final String storageLocation;
  final DateTime? expiryDate;
  final DateTime? purchaseDate;
  final DateTime? openedDate;
  final String? barcode;
  final String? imageUrl;
  final String? notes;
  final String status;
  final int? daysUntilExpiry;

  InventoryItem({
    required this.id,
    required this.productName,
    required this.category,
    this.brand,
    required this.quantity,
    required this.unit,
    required this.storageLocation,
    this.expiryDate,
    this.purchaseDate,
    this.openedDate,
    this.barcode,
    this.imageUrl,
    this.notes,
    required this.status,
    this.daysUntilExpiry,
  });

  factory InventoryItem.fromJson(Map<String, dynamic> json) {
    return InventoryItem(
      id: json['id'],
      productName: json['product_name'] ?? '',
      category: json['category'] ?? 'Other',
      brand: json['brand'],
      quantity: (json['quantity'] as num).toDouble(),
      unit: json['unit'] ?? 'pcs',
      storageLocation: json['storage_location'] ?? 'Pantry',
      expiryDate: json['expiry_date'] != null ? DateTime.tryParse(json['expiry_date']) : null,
      purchaseDate: json['purchase_date'] != null ? DateTime.tryParse(json['purchase_date']) : null,
      openedDate: json['opened_date'] != null ? DateTime.tryParse(json['opened_date']) : null,
      barcode: json['barcode'],
      imageUrl: json['image_url'],
      notes: json['notes'],
      status: json['status'] ?? 'Healthy',
      daysUntilExpiry: json['days_until_expiry'],
    );
  }
}

class BarcodeResult {
  final bool found;
  final String barcode;
  final String? productName;
  final String? brand;
  final String? category;
  final String? imageUrl;
  final String? defaultUnit;

  BarcodeResult({
    required this.found,
    required this.barcode,
    this.productName,
    this.brand,
    this.category,
    this.imageUrl,
    this.defaultUnit,
  });

  factory BarcodeResult.fromJson(Map<String, dynamic> json) {
    return BarcodeResult(
      found: json['found'] ?? false,
      barcode: json['barcode'] ?? '',
      productName: json['product_name'],
      brand: json['brand'],
      category: json['category'],
      imageUrl: json['image_url'],
      defaultUnit: json['default_unit'] ?? 'pcs',
    );
  }
}

class OCRResult {
  final bool detected;
  final String? productName;
  final String? brand;
  final String? expiryDate;
  final String? mfgDate;
  final double? quantity;
  final String? unit;
  final String? batchNumber;
  final double confidenceScore;

  OCRResult({
    required this.detected,
    this.productName,
    this.brand,
    this.expiryDate,
    this.mfgDate,
    this.quantity,
    this.unit,
    this.batchNumber,
    required this.confidenceScore,
  });

  factory OCRResult.fromJson(Map<String, dynamic> json) {
    return OCRResult(
      detected: json['detected'] ?? false,
      productName: json['product_name'],
      brand: json['brand'],
      expiryDate: json['expiry_date'],
      mfgDate: json['mfg_date'],
      quantity: json['quantity'] != null ? (json['quantity'] as num).toDouble() : 1.0,
      unit: json['unit'] ?? 'pcs',
      batchNumber: json['batch_number'],
      confidenceScore: json['confidence_score'] != null ? (json['confidence_score'] as num).toDouble() : 0.0,
    );
  }
}

class RecommendationItem {
  final int id;
  final String productName;
  final String category;
  final double suggestedQuantity;
  final String unit;
  final String reason;
  final String urgency;
  final bool addedToCart;

  RecommendationItem({
    required this.id,
    required this.productName,
    required this.category,
    required this.suggestedQuantity,
    required this.unit,
    required this.reason,
    required this.urgency,
    required this.addedToCart,
  });

  factory RecommendationItem.fromJson(Map<String, dynamic> json) {
    return RecommendationItem(
      id: json['id'],
      productName: json['product_name'] ?? '',
      category: json['category'] ?? 'Other',
      suggestedQuantity: (json['suggested_quantity'] as num).toDouble(),
      unit: json['unit'] ?? 'pcs',
      reason: json['reason'] ?? '',
      urgency: json['urgency'] ?? 'Medium',
      addedToCart: json['added_to_cart'] ?? false,
    );
  }
}

class CartItemModel {
  final int id;
  final String productName;
  final double quantity;
  final String unit;
  final double estimatedPrice;
  final String? reason;
  final String priority;
  final bool confirmed;

  CartItemModel({
    required this.id,
    required this.productName,
    required this.quantity,
    required this.unit,
    required this.estimatedPrice,
    this.reason,
    required this.priority,
    required this.confirmed,
  });

  factory CartItemModel.fromJson(Map<String, dynamic> json) {
    return CartItemModel(
      id: json['id'],
      productName: json['product_name'] ?? '',
      quantity: (json['quantity'] as num).toDouble(),
      unit: json['unit'] ?? 'pcs',
      estimatedPrice: (json['estimated_price'] as num).toDouble(),
      reason: json['reason'],
      priority: json['priority'] ?? 'Normal',
      confirmed: json['confirmed'] ?? false,
    );
  }
}

class SmartCartModel {
  final int id;
  final int householdId;
  final double totalEstimatedPrice;
  final String status;
  final List<CartItemModel> items;

  SmartCartModel({
    required this.id,
    required this.householdId,
    required this.totalEstimatedPrice,
    required this.status,
    required this.items,
  });

  factory SmartCartModel.fromJson(Map<String, dynamic> json) {
    var rawItems = json['items'] as List? ?? [];
    List<CartItemModel> itemList = rawItems.map((i) => CartItemModel.fromJson(i)).toList();
    return SmartCartModel(
      id: json['id'],
      householdId: json['household_id'],
      totalEstimatedPrice: (json['total_estimated_price'] as num).toDouble(),
      status: json['status'] ?? 'active',
      items: itemList,
    );
  }
}

class NotificationItem {
  final int id;
  final String title;
  final String message;
  final String type;
  final String priority;
  final bool isRead;
  final DateTime createdAt;

  NotificationItem({
    required this.id,
    required this.title,
    required this.message,
    required this.type,
    required this.priority,
    required this.isRead,
    required this.createdAt,
  });

  factory NotificationItem.fromJson(Map<String, dynamic> json) {
    return NotificationItem(
      id: json['id'],
      title: json['title'] ?? '',
      message: json['message'] ?? '',
      type: json['type'] ?? 'expiry',
      priority: json['priority'] ?? 'normal',
      isRead: json['is_read'] ?? false,
      createdAt: DateTime.tryParse(json['created_at'] ?? '') ?? DateTime.now(),
    );
  }
}

class AIInsightSummaryModel {
  final int healthyCount;
  final int expiringSoonCount;
  final int expiredCount;
  final int runningLowCount;
  final double foodWasteEstimate;
  final String topConsumedCategory;
  final String recentInsightMessage;

  AIInsightSummaryModel({
    required this.healthyCount,
    required this.expiringSoonCount,
    required this.expiredCount,
    required this.runningLowCount,
    required this.foodWasteEstimate,
    required this.topConsumedCategory,
    required this.recentInsightMessage,
  });

  factory AIInsightSummaryModel.fromJson(Map<String, dynamic> json) {
    return AIInsightSummaryModel(
      healthyCount: json['healthy_count'] ?? 0,
      expiringSoonCount: json['expiring_soon_count'] ?? 0,
      expiredCount: json['expired_count'] ?? 0,
      runningLowCount: json['running_low_count'] ?? 0,
      foodWasteEstimate: (json['food_waste_estimate'] as num).toDouble(),
      topConsumedCategory: json['top_consumed_category'] ?? 'Dairy',
      recentInsightMessage: json['recent_insight_message'] ?? '',
    );
  }
}
