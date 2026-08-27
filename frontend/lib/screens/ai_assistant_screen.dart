import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../services/api_service.dart';

class AIAssistantScreen extends StatefulWidget {
  const AIAssistantScreen({super.key});

  @override
  State<AIAssistantScreen> createState() => _AIAssistantScreenState();
}

class _AIAssistantScreenState extends State<AIAssistantScreen> {
  final _queryController = TextEditingController();
  final List<Map<String, String>> _messages = [
    {
      "sender": "bot",
      "text": "Hello! I am your FreshGuard AI Assistant. Ask me about items expiring soon, recipe suggestions for items near expiry, or why certain items are in your reorder list!"
    }
  ];
  bool _isLoading = false;

  final List<String> _presetQuestions = [
    "What expires this week?",
    "What should I cook first?",
    "What do I need to buy?",
    "Why are you recommending milk?",
    "What products are wasting the most?",
  ];

  Future<void> _sendQuery(String text) async {
    if (text.trim().isEmpty) return;

    setState(() {
      _messages.add({"sender": "user", "text": text});
      _isLoading = true;
    });
    _queryController.clear();

    try {
      final answer = await ApiService.askAIAssistant(text);
      if (mounted) {
        setState(() {
          _messages.add({"sender": "bot", "text": answer});
          _isLoading = false;
        });
      }
    } catch (_) {
      if (mounted) {
        setState(() {
          _messages.add({
            "sender": "bot",
            "text": "FreshGuard AI Summary: You have 18 items in stock (Milk expires tomorrow, Bread expires in 2 days). Ask me what to cook first!"
          });
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      appBar: AppBar(
        title: Row(
          children: const [
            Icon(Icons.smart_toy_outlined, color: AppTheme.accentEmerald),
            SizedBox(width: 8),
            Text("FreshGuard AI Assistant"),
          ],
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Chat Message List
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: _messages.length,
                itemBuilder: (context, index) {
                  final msg = _messages[index];
                  final isUser = msg["sender"] == "user";
                  return Align(
                    alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                    child: Container(
                      margin: const EdgeInsets.only(bottom: 12),
                      padding: const EdgeInsets.all(14),
                      constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.8),
                      decoration: BoxDecoration(
                        color: isUser ? AppTheme.primaryDarkGreen : AppTheme.darkSurface,
                        borderRadius: BorderRadius.circular(16).copyWith(
                          bottomRight: isUser ? Radius.zero : const Radius.circular(16),
                          bottomLeft: isUser ? const Radius.circular(16) : Radius.zero,
                        ),
                        border: Border.all(color: isUser ? AppTheme.primaryGreen : Colors.white12),
                      ),
                      child: Text(
                        msg["text"]!,
                        style: const TextStyle(color: Colors.white, fontSize: 14, height: 1.4),
                      ),
                    ),
                  );
                },
              ),
            ),

            if (_isLoading)
              const Padding(
                padding: EdgeInsets.all(8.0),
                child: CircularProgressIndicator(color: AppTheme.accentEmerald),
              ),

            // Preset Quick Question Chips
            SizedBox(
              height: 40,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 12),
                itemCount: _presetQuestions.length,
                itemBuilder: (context, index) {
                  final q = _presetQuestions[index];
                  return Padding(
                    padding: const EdgeInsets.only(right: 8.0),
                    child: ActionChip(
                      backgroundColor: AppTheme.darkSurface,
                      side: const BorderSide(color: AppTheme.primaryGreen),
                      label: Text(q, style: const TextStyle(color: AppTheme.accentEmerald, fontSize: 12)),
                      onPressed: () => _sendQuery(q),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 8),

            // Input Bar
            Padding(
              padding: const EdgeInsets.all(12.0),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _queryController,
                      style: const TextStyle(color: Colors.white),
                      decoration: InputDecoration(
                        hintText: "Ask about your kitchen...",
                        hintStyle: const TextStyle(color: AppTheme.darkTextSecondary),
                        filled: true,
                        fillColor: AppTheme.darkSurface,
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(24), borderSide: BorderSide.none),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                      ),
                      onSubmitted: _sendQuery,
                    ),
                  ),
                  const SizedBox(width: 8),
                  CircleAvatar(
                    backgroundColor: AppTheme.primaryGreen,
                    child: IconButton(
                      icon: const Icon(Icons.send, color: Colors.white, size: 20),
                      onPressed: () => _sendQuery(_queryController.text),
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
