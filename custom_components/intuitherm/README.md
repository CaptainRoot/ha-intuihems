# intuiHEMS - Smart Battery Optimizer

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/intui/intuiHEMS.svg)](https://github.com/intui/ha-intuihems/releases/)

> **Spare Stromkosten & reduziere CO₂** - Dein Batteriespeicher wird automatisch zum optimalen Zeitpunkt gesteuert.

**intuiHEMS** ist ein Smart Battery Optimizer für Home Assistant. Es optimiert deinen Heimspeicher anhand dynamischer Strompreise, Solarprognosen und deines Verbrauchs vollautomatisch.

## ✨ Das sind die Vorteile

- **💰 Kosten senken:** Die Batterie wird bei günstigen Strompreisen geladen und versorgt dein Zuhause bei hohen Preisen aus dem Speicher.

- **🌱 Mehr erneuerbare Energie nutzen:** Die Batterie lädt bevorzugt, wenn viel grüner Strom verfügbar ist.

- **⚡ Netz entlasten:** Lastspitzen werden vermieden, indem teurer und netzbelastender Strom nicht genutzt wird.

- **🤖 Kostenlos & ohne Aufwand:** intuiHEMS ist kostenlos downloadbar und plant den Betrieb deines Speichers vollständig automatisch.

## 🧠 Wie intuiHEMS deinen Speicher optimiert

intuiHEMS erkennt deinen Batteriespeicher, deine PV-Anlage und den Hausverbrauch automatisch, ganz ohne aufwendige Einrichtung.

Mithilfe KI-gestützter Prognosen berechnet das System bis zu 24 Stunden im Voraus, wie sich Stromverbrauch, Solarertrag und Strompreise entwickeln. Auf dieser Basis wird alle 15 Minuten ein optimaler Lade- und Entladeplan erstellt.

So wird dein Speicher genau dann geladen oder genutzt, wenn es wirtschaftlich und ökologisch sinnvoll ist. In deinem Home-Assistant-Dashboard siehst du jederzeit, wie viel Geld und CO₂ du dadurch einsparst.

**Deine Daten bleiben dabei vollständig in deiner Kontrolle und werden nicht an Dritte weitergegeben.**

## ⚠️ Alpha-Version

intuiHEMS befindet sich aktuell in der Alpha-Phase. Die Kernfunktionen sind stabil, dennoch können vereinzelt Bugs auftreten.

Während der Alpha-Phase ist das Plugin kostenlos und auf **100 Tester limitiert**. Ziel ist es, durch kontinuierliche Weiterentwicklung Stromkosten um **20–40 %** zu senken. Feedback aus der Community spielt dabei eine zentrale Rolle.

## 📋 Voraussetzungen

intuiHEMS funktioniert, wenn folgende Punkte erfüllt sind:

- Home Assistant (Version 2024.4 oder neuer)
- Batteriespeicher mit bestehender Home-Assistant-Integration
- Energy Dashboard ist eingerichtet
- Internetverbindung für Prognosen & Optimierung

## 🚀 Installation

### 1. Über HACS installieren
HACS → Integrationen → „intuiHEMS" suchen → Installieren

### 2. Integration hinzufügen
Einstellungen → Geräte & Dienste → intuiHEMS

### 3. Fertig ✨
Dein Batteriespeicher wird jetzt automatisch optimiert.

---

**Hinweis:** Systeme die nicht automatisch erkannt werden, können manuell angebunden werden.

**Mit ❤️ für die Home Assistant Community**