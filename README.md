# Prompt-Engineers-x3
AI-powered Smart Waste Detection System using YOLOv8 that classifies garbage in real-time through camera input to enable automated waste segregation and smart recycling.
# ♻️ Smart Waste Segregation AI
# Problem Statement: PS2

## 📌 Project Overview

Smart Waste Segregation AI is an AI-powered system that detects and classifies garbage into different categories using computer vision. This solution helps automate waste segregation, promoting efficient recycling and sustainable waste management.

The system uses a trained YOLOv8 model to identify waste items in real-time through a webcam.

---

## 🎯 Problem Statement

Manual waste segregation is inefficient and often leads to improper recycling. Our solution automates waste classification using AI to improve recycling efficiency and reduce environmental impact.

---

## 🧠 Model Used

* **Model:** YOLOv8 (Ultralytics)
* **Framework:** PyTorch
* **Language:** Python
* **Backend:** Flask
* **Frontend:** HTML, CSS, JavaScript

---

## 📂 Dataset Used

Dataset: Garbage Dataset – A Comprehensive Image Dataset for Garbage Classification

### Classes

* Plastic
* Paper
* Cardboard
* Glass
* Metal
* Trash
* Organic
* E-waste
* Textile
* Other Waste

### Preprocessing

* Image resizing
* Data augmentation
* Train / Validation split
* Label normalization

---

## ⚙️ Features

✅ Real-time waste detection
✅ AI-based garbage classification
✅ Webcam integration
✅ Fast YOLOv8 inference
✅ Easy to deploy locally
✅ Eco-friendly waste guidance

---

## 📊 Model Performance

* Training Epochs: 10
* Model: YOLOv8n
* Accuracy: ~80–90% (approx depending on dataset)
* Real-time detection speed

---

## 🏗️ Project Structure

```
smart-bin-ai
│
├── backend
│   ├── app.py
│   ├── best.pt
│   └── dataset.yaml
│
├── frontend
│   └── index.html
│
└── README.md
```

---

## 🚀 How to Run

### Step 1 — Install Dependencies

```
pip install ultralytics flask opencv-python numpy
```

### Step 2 — Run Backend

```
python backend/app.py
```

### Step 3 — Open Browser

```
http://localhost:5000
```

---

## 📸 Output

The system detects garbage in real-time and classifies into categories:

Example:

* Plastic Bottle → Plastic
* Paper Sheet → Paper
* Glass Bottle → Glass

---

## 🎥 Demo Video

(Upload demo video under 4 minutes here)

---

## 💡 Future Improvements

* Mobile App Integration
* Smart Dustbin Hardware
* Cloud Deployment
* Accuracy Optimization
* IoT Smart Bin Integration

---

## 🌍 Impact

* Improves recycling efficiency
* Reduces landfill waste
* Promotes sustainability
* Smart city implementation ready

---

## 👨‍💻 Team Prompt-Engineers-x3

AI-powered Smart Waste Segregation System for Sustainable Future ♻️

---

## 📎 Submission

GitHub Repository: https://github.com/ansysyadav40-a11y/Prompt-Engineers-x3
