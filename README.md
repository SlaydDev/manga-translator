![Slayd Development Shutdown](https://img.shields.io/badge/Slayd%20Development%20Has%20Been%20Shutdown-%20Migrated%20to%20CaptainEXE%20Studios-red?style=for-the-badge)

# 📖 Manga Translator

A modern **AI-powered manga translation tool** built with Streamlit, combining image OCR and large language models to extract and localize Japanese manga panels into clean English output.

The system uses a two-stage pipeline: visual text extraction followed by contextual translation, designed specifically for preserving dialogue structure and reading flow in manga layouts.

---

## 🚀 Features

### 🧠 AI Translation Pipeline

* Extracts text from manga images using **Google Gemini**
* Converts raw OCR output into natural English using **Groq LLaMA 3**
* Maintains dialogue structure and reading order

### 🖼️ Image Input Options

* Upload manga pages (`.jpg`, `.png`, `.jpeg`)
* Capture directly using camera input
* Supports full panel processing

### ⚙️ Dual Processing Modes

* **ECO Mode** → Raw translated text output
* **PRO Mode** → Visual preview + structured translation overlay

### 🎨 Modern UI System

* Catppuccin Mocha-inspired design
* Animated boot splash screen
* Glass-style UI cards
* Responsive layout for desktop use

### 🔐 Secure Key-Based Access

* Gemini API authentication
* Groq API authentication
* Session-based secure runtime handling

---

## 🛠️ Tech Stack

| Component                     | Purpose                    |
| ----------------------------- | -------------------------- |
| Streamlit                     | Web UI framework           |
| Google Generative AI (Gemini) | OCR & text extraction      |
| Groq API (LLaMA 3.1)          | Translation & localization |
| PIL (Pillow)                  | Image processing           |
| Python                        | Core backend logic         |

---

## 📂 Project Structure

```file sytem
Manga-Translator/
├─ app.py
├─ requirements.txt
├─ assets/
│  ├─ logo.png
│  ├─ styles.css (optional)
└─ README.md
```

---

## ⚙️ How It Works

### 1. Authentication Layer

Users provide:

* Google Gemini API key
* Groq API key

These are stored in session state for runtime processing.

### 2. OCR Extraction

The uploaded manga image is processed using Gemini with a structured prompt designed to:

* Detect dialogue bubbles
* Extract narration text
* Preserve right-to-left reading structure

### 3. Translation Layer

The extracted raw text is passed into LLaMA 3.1 via Groq API, which:

* Localizes Japanese text into English
* Preserves tone and conversational structure
* Rewrites dialogue naturally

### 4. Output Rendering

Depending on mode:

* ECO → plain translated text
* PRO → image + structured text overlay

---

## 🎯 Use Cases

* Manga translation practice tools
* AI-assisted localization workflows
* OCR + LLM pipeline experiments
* Educational NLP projects
* Image-to-text research systems

---

## 🔐 Requirements

Install dependencies:

```bash
pip install streamlit google-generativeai groq pillow
```

---

## 🚀 Running the App

```bash
streamlit run app.py
```

---

## 📌 Notes

* Requires valid API keys for both Gemini and Groq
* Optimized for manga-style structured text (not general document OCR)
* Performance depends on image clarity and panel layout

---

## 🧠 Design Philosophy

This project is built around a simple idea:

> Extract structure first, then translate meaning.

Instead of treating manga as plain text, it preserves layout hierarchy, dialogue flow, and narrative structure before translation.

---

## 📜 License

Educational / experimental use only.

---

## 👨‍💻 Maintained By

**CaptainEXE**
https://github.com/itscaptainexe
https://captainexe.vercel.app
