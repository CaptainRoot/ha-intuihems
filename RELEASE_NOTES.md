# Release v2025.11.9 - Device Learning System

## 🎉 Major Features

### Device-Based Auto-Detection
Automatically detects battery control entities for major inverter brands:
- ✅ **FoxESS** (verified from production)
- ✅ **Solis**
- ✅ **Huawei**
- ✅ **SolarEdge**
- ✅ **Growatt**

### Community Device Learning
- 📚 Local storage of learned device configurations
- 🌍 Optional community sharing for pattern matching
- 📊 Success rate tracking
- 🔒 Privacy-first: only patterns shared, not entity IDs

### Simplified Setup Flow
- 🎯 Version display on welcome screen
- ⚙️ Hard-coded service URL and API key for alpha testing
- 🚀 Zero-configuration for supported inverters
- 📱 Streamlined user experience

## 🔧 Technical Improvements

### Home Assistant Services
- `intuitherm.list_learned_devices` - View all learned device configurations
- `intuitherm.delete_learned_device` - Remove learned device by index
- `intuitherm.export_learned_devices` - Export configurations as JSON

### Configuration Storage
- Persistent local storage via HA Store API
- Device info extraction from entity registry
- Pattern matching with substring support for model variants

## 📚 Documentation

- [Device Learning System Guide](docs/DEVICE_LEARNING_SYSTEM.md)
- [Device-Based Auto-Detection](docs/DEVICE_BASED_AUTODETECTION.md)
- [Alpha Testing Guide](ALPHA_TESTING_GUIDE.md)

## 🐛 Bug Fixes

- Fixed HACS repository URLs in manifest
- Updated integration name to "intuiHEMS" consistently
- Removed manual service URL/API key input for alpha phase

## 📦 Installation

### Via HACS (Custom Repository)
1. HACS → Integrations → ⋮ → Custom repositories
2. Add: `https://github.com/intui/intuitherm`
3. Category: Integration
4. Search "intuiHEMS" and install
5. Restart Home Assistant

### Manual
Download and extract to `config/custom_components/intuitherm/`

## ⚡ Quick Start

1. Add Integration: Settings → Devices & Services → Add Integration → "intuiHEMS"
2. Click through welcome screen (shows version)
3. Auto-detection runs automatically
4. Review and confirm sensors
5. Battery controls auto-detected (if supported inverter)
6. Done! ✨

## 🎯 What's Next

### v2025.12.0 (Planned)
- [ ] Merge to main branch
- [ ] Official HACS default repository submission
- [ ] Community API backend for device sharing
- [ ] UI for opt-in/opt-out preferences
- [ ] Additional inverter brand support

## 🙏 Contributors

- Core development: @intui
- Alpha testers: (add your name!)
- FoxESS pattern verified from production deployment

## 📞 Support

- 🐛 [Report bugs](https://github.com/intui/intuitherm/issues)
- 💡 [Feature requests](https://github.com/intui/intuitherm/issues)
- 💬 [Discussions](https://github.com/intui/intuitherm/discussions)

---

**Full Changelog**: https://github.com/intui/intuitherm/compare/v2025.11.4.2...v2025.11.9
