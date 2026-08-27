import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../services/api_service.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _householdController = TextEditingController(text: "My Kitchen");
  bool _isLoading = false;
  String? _errorMessage;

  Future<void> _handleRegister() async {
    if (_emailController.text.isEmpty || _passwordController.text.isEmpty) {
      setState(() => _errorMessage = "Email and password are required");
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      await ApiService.register(
        _emailController.text.trim(),
        _passwordController.text.trim(),
        _nameController.text.trim(),
        _householdController.text.trim(),
      );
      if (mounted) {
        Navigator.pushReplacementNamed(context, '/home');
      }
    } catch (e) {
      setState(() => _errorMessage = e.toString().replaceAll("Exception: ", ""));
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
      appBar: AppBar(backgroundColor: Colors.transparent),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                "Create Account 🚀",
                style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white),
              ),
              const SizedBox(height: 8),
              const Text(
                "Start tracking food, eliminating waste, and automating grocery refills.",
                style: TextStyle(color: AppTheme.darkTextSecondary, fontSize: 14),
              ),
              const SizedBox(height: 24),

              if (_errorMessage != null) ...[
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(_errorMessage!, style: const TextStyle(color: Colors.red)),
                ),
                const SizedBox(height: 16),
              ],

              TextField(
                controller: _nameController,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: "Full Name",
                  labelStyle: const TextStyle(color: AppTheme.darkTextSecondary),
                  prefixIcon: const Icon(Icons.person_outline, color: AppTheme.primaryGreen),
                  filled: true,
                  fillColor: AppTheme.darkSurface,
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _householdController,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: "Household Name",
                  labelStyle: const TextStyle(color: AppTheme.darkTextSecondary),
                  prefixIcon: const Icon(Icons.home_outlined, color: AppTheme.primaryGreen),
                  filled: true,
                  fillColor: AppTheme.darkSurface,
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _emailController,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: "Email Address",
                  labelStyle: const TextStyle(color: AppTheme.darkTextSecondary),
                  prefixIcon: const Icon(Icons.email_outlined, color: AppTheme.primaryGreen),
                  filled: true,
                  fillColor: AppTheme.darkSurface,
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                ),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _passwordController,
                obscureText: true,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: "Password",
                  labelStyle: const TextStyle(color: AppTheme.darkTextSecondary),
                  prefixIcon: const Icon(Icons.lock_outline, color: AppTheme.primaryGreen),
                  filled: true,
                  fillColor: AppTheme.darkSurface,
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                ),
              ),
              const SizedBox(height: 24),

              SizedBox(
                width: double.infinity,
                height: 52,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _handleRegister,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppTheme.primaryGreen,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  child: _isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text("Create Household Account", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
