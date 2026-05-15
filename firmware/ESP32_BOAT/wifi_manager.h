#ifndef WIFI_MANAGER_H
#define WIFI_MANAGER_H

#include <WiFi.h>
#include "config.h"

// ─────────────────────────────
// WiFi Setup
// ─────────────────────────────
void wifiSetup()
{
    Serial.println("[WIFI] Connecting to: " + String(WIFI_SSID));

    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 30)
    {
        delay(500);
        Serial.print(".");
        attempts++;
    }

    if (WiFi.status() == WL_CONNECTED)
    {
        Serial.println();
        Serial.println("================================");
        Serial.println("[WIFI] Connected Successfully!");
        Serial.println("[WIFI] IP  : " + WiFi.localIP().toString());
        Serial.println("[WIFI] RSSI: " + String(WiFi.RSSI()) + " dBm");
        Serial.println("[WIFI] MAC : " + WiFi.macAddress());
        Serial.println("================================");
    }
    else
    {
        Serial.println();
        Serial.println("[WIFI] Failed! Check SSID/Password in config.h");
    }
}

// ─────────────────────────────
// WiFi Loop Handler
// (auto-reconnect)
// ─────────────────────────────
void wifiHandle()
{
    static unsigned long lastCheck = 0;

    if (millis() - lastCheck < 10000)
        return;

    lastCheck = millis();

    if (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("[WIFI] Disconnected! Reconnecting...");
        WiFi.disconnect();
        WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    }
}

// ─────────────────────────────
// WiFi Connection Status
// ─────────────────────────────
bool isWifiConnected()
{
    return WiFi.status() == WL_CONNECTED;
}

// ─────────────────────────────
// Get Backend URL
// ─────────────────────────────
String getBackendURL()
{
    return String(BACKEND_URL);
}

#endif
