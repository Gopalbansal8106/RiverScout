# 🌊 RiverScout – AI-Powered IoT System for Real-Time River Health Monitoring

## 📌 Overview
RiverScout is an IoT-based system designed to monitor river health in real time using sensor data and geospatial tracking. The system collects environmental parameters, transmits them to a backend server, and visualizes insights through an interactive dashboard. It also integrates AI-driven analysis to detect anomalies and provide actionable insights for environmental monitoring.

---

## 🚀 Features
- 📡 Real-time data collection using sensors  
- 📍 GPS-based location tracking and mapping  
- 📊 Interactive dashboard with live visualization  
- 🤖 AI-based anomaly detection and advisory system  
- 🌐 Web interface for monitoring and analysis  

---

## 🏗️ System Architecture

### Hardware Layer
- ESP32 / Arduino  
- Environmental sensors (water quality parameters)  
- GPS module  

### Backend Layer
- Data ingestion via HTTP/MQTT  
- Flask server  
- Data processing and storage  

### Frontend Layer
- Dashboard for visualization  
- Maps integration (Leaflet)  
- Charts for real-time monitoring  

---

## 🛠️ Technologies Used
- **Hardware:** ESP32, Arduino, Sensors, GPS  
- **Backend:** Flask, REST APIs  
- **Frontend:** HTML, CSS, JavaScript, Chart.js, Leaflet  
- **AI/ML:** Basic anomaly detection, Gemini API  

---

## ⚙️ How It Works
1. Sensors collect river parameters (temperature, pH, turbidity)  
2. Data is transmitted via ESP32 to backend  
3. Backend processes and stores data  
4. Dashboard displays real-time insights  
5. AI module detects anomalies and suggests actions  
