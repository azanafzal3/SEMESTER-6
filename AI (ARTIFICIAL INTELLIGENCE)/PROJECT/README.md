
# 🎬 AI Movie Summary Analyzer

A Streamlit-based interactive application that performs:
- 🎯 **Movie Genre Prediction** using a fine-tuned `Logistic Regression` + `SentenceTransformer` model.
- 🔊 **Text-to-Speech Audio Generation** with **language translation** using Microsoft Edge TTS and Google Translate.

---

## 📁 Project Structure

```
AI_Movie_Summary_Analyzer/
│
├── gui_app.py                       # Main Streamlit GUI Application
├── genre_classifier_cleaned.pkl    # Trained classification model
├── label_binarizer_cleaned.pkl     # Label binarizer for genre multi-label encoding
├── AI Generated Work/              # Folder to store generated genres and audio (optional)
├── requirements.txt                # All Python dependencies
├── README.md                       # Project documentation
├── train_data.csv                  # (If retraining is needed)
├── test_data.csv                   # (If retraining is needed)
```

---

## ✅ Dependencies

Install the dependencies using:

```bash
pip install -r requirements.txt
```

**requirements.txt**
```txt
streamlit
edge-tts
sentence-transformers
scikit-learn
joblib
matplotlib
seaborn
googletrans==4.0.0rc1
```

If using Python ≥ 3.11 and facing `cgi`-related issues, replace `googletrans` with another lightweight translation library or patch the library.

---

## ▶️ How to Run

```bash
streamlit run gui_app.py
```

---

## ✍ Features

### 1. **Genre Prediction**
- Enter a movie summary.
- The app predicts the **top 3 genres** using a trained model (`genre_classifier_cleaned.pkl`).
- Predicted genres are also saved into the `AI Generated Work` folder as a text file.

### 2. **Summary-to-Audio**
- Select from **English**, **Urdu**, **Arabic**, or **Korean**.
- The app **translates** your summary first using Google Translate.
- Then generates audio using **Microsoft Edge TTS**.
- Users can choose to **play or download** the audio.

---

## 🧠 Model Details

- Embeddings via: `all-MiniLM-L6-v2` (SentenceTransformer)
- Classifier: `LogisticRegression` in a `OneVsRestClassifier` wrapper
- Multi-label target encoding via `MultiLabelBinarizer`

---


