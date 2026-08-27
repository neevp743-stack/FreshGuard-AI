import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../services/api_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController(text: "demo@freshguard.ai");
  final _passwordController = TextEditingController(text: "password123");
  bool _isLoading = false;
  String? _errorMessage;

  Future<void> _handleLogin({bool isDemo = false}) async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final email = isDemo ? "demo@freshguard.ai" : _emailController.text.trim();
      final pass = isDemo ? "password123" : _passwordController.text.trim();
      
      await ApiService.login(email, pass);
      if (mounted) {
        Navigator.pushReplacementNamed(context, '/home');
      }
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll("Exception: ", "");
        // Fallback for offline demo preview
        if (isDemo) {
          Navigator.pushReplacementNamed(context, '/home');
        }
      });
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
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 32),
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppTheme.primaryGreen.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(Icons.shield, color: AppTheme.primaryGreen, size: 32),
                  ),
                  const SizedBox(width: 12),
                  const Text(
                    "FreshGuard AI",
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white),
                  ),
                ],
              ),
              const SizedBox(height: 32),
              const Text(
                "Welcome Back 👋",
                style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white),
              ),
              const SizedBox(height: 8),
              const Text(
                "Sign in to manage your household grocery inventory & AI recommendations.",
                style: TextStyle(color: AppTheme.darkTextSecondary, fontSize: 14),
              ),
              const SizedBox(height: 32),

              if (_errorMessage != null) ...[
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.red.withOpacity(0.5)),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.error_outline, color: Colors.red, size: 20),
                      const SizedBox(width: 8),
                      Expanded(child: Text(_errorMessage!, style: const TextStyle(color: Colors.red))),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
              ],

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
                  onPressed: _isLoading ? null : () => _handleLogin(),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppTheme.primaryGreen,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  child: _isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text("Sign In", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                ),
              ),
              const SizedBox(height: 12),

              // Demo Account Button
              SizedBox(
                width: double.infinity,
                height: 52,
                child: OutlinedButton.icon(
                  onPressed: _isLoading ? null : () => _handleLogin(isDemo: true),
                  icon: const Icon(Icons.flash_on, color: AppTheme.accentEmerald),
                  label: const Text("Explore Live Demo Mode", style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600, color: AppTheme.accentEmerald)),
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: AppTheme.accentEmerald),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                ),
              ),
              const SizedBox(height: 24),

              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text("Don't have an account? ", style: TextStyle(color: AppTheme.darkTextSecondary)),
                  GestureDetector(
                    onTap: () => Navigator.pushNamed(context, '/register'),
                    child: const Text("Register", style: TextStyle(color: AppTheme.primaryGreen, fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
