import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  bool _expiryAlerts = true;
  bool _runoutAlerts = true;
  bool _darkMode = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      appBar: AppBar(title: const Text("Profile & Settings")),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // User Profile Header
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppTheme.darkSurface,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Row(
                  children: [
                    CircleAvatar(
                      radius: 30,
                      backgroundColor: AppTheme.primaryGreen,
                      child: const Text("AM", style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white)),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: const [
                          Text("Alex Morgan", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
                          SizedBox(height: 4),
                          Text("demo@freshguard.ai", style: TextStyle(color: AppTheme.darkTextSecondary, fontSize: 13)),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Household Code Card
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppTheme.primaryDarkGreen.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: AppTheme.primaryGreen),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: const [
                        Text("Household: Morgan Family", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                        SizedBox(height: 4),
                        Text("Join Code: FG-DEMO26", style: TextStyle(color: AppTheme.accentEmerald, fontWeight: FontWeight.bold)),
                      ],
                    ),
                    IconButton(
                      icon: const Icon(Icons.copy, color: AppTheme.accentEmerald),
                      onPressed: () {
                        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Join code copied to clipboard!")));
                      },
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              const Text("Notification Preferences", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
              const SizedBox(height: 12),
              SwitchListTile(
                tileColor: AppTheme.darkSurface,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                title: const Text("Expiry Warnings", style: TextStyle(color: Colors.white)),
                subtitle: const Text("Notify 7, 3, and 1 day before expiry", style: TextStyle(color: AppTheme.darkTextSecondary, fontSize: 12)),
                activeColor: AppTheme.primaryGreen,
                value: _expiryAlerts,
                onChanged: (val) => setState(() => _expiryAlerts = val),
              ),
              const SizedBox(height: 8),
              SwitchListTile(
                tileColor: AppTheme.darkSurface,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                title: const Text("Run-out Predictions", style: TextStyle(color: Colors.white)),
                subtitle: const Text("Notify before essential products run out", style: TextStyle(color: AppTheme.darkTextSecondary, fontSize: 12)),
                activeColor: AppTheme.primaryGreen,
                value: _runoutAlerts,
                onChanged: (val) => setState(() => _runoutAlerts = val),
              ),
              const SizedBox(height: 24),

              const Text("Grocery Integration Architecture", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white)),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppTheme.darkSurface,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Row(
                  children: const [
                    Icon(Icons.api, color: Colors.amber, size: 24),
                    SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        "Provider Status: Mock Grocery Provider Active.\nArchitecture is ready for future official delivery APIs.",
                        style: TextStyle(color: Colors.white70, fontSize: 12, height: 1.4),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 32),

              SizedBox(
                width: double.infinity,
                height: 50,
                child: OutlinedButton.icon(
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: Colors.redAccent),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  onPressed: () => Navigator.pushReplacementNamed(context, '/login'),
                  icon: const Icon(Icons.logout, color: Colors.redAccent),
                  label: const Text("Sign Out", style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
