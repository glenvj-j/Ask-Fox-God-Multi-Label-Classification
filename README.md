# 🎸 Ask FOX GOD - Multi-Label Setlist Prediction Project

![Cover](https://github.com/user-attachments/assets/6b4ba631-4519-497a-93a0-a3a604217648)


> [!NOTE]
> Dashboard : [View Tableau](https://public.tableau.com/app/profile/glen.joy2546/viz/AskFoxGod/Dashboard1)<br>
> Presentation Deck  : [View Google Slides](https://docs.google.com/presentation/d/1pu_2hJgoMdNEtERQIvfJATNQTGxtS9sFaBmORvzGE-0/edit?slide=id.p#slide=id.p)<br>
> Deployment : [View here](https://civdexai-new.streamlit.app/)

This project aims to build and deploy a **multi-label classification model** to predict the likely setlist of BABYMETAL songs in concerts. We also provide an interactive **Streamlit web app** and a **performance dashboard** to explore model predictions and insights.

---

## 🚀 Project Overview

BABYMETAL, known for dynamic performances and rotating setlists, presents an interesting multi-label prediction challenge. Given metadata about a concert (e.g., location, date, and album status), the goal is to predict **multiple songs** likely to be played in that concert.

The data is scrapped from [setlist.fm](https://www.setlist.fm/setlists/babymetal-5bd19f80.html)

You can see how I scrapped by open the Notebook called Scrapping Using API.ipynb

### 💡 Problem Type
- **Multi-Label Classification** (a concert can include multiple songs from a predefined list)

---

## 🧠 Model Performance

The final model was evaluated using appropriate multi-label metrics:

| Metric             | Score  |
|--------------------|--------|
| Precision (micro)  | 0.819  |
| Hamming Loss       | 0.052  |

This indicates that the model can predict song combinations with high accuracy and minimal label-wise error.

---

## 🛠️ Features

- 🎵 **Multi-label song prediction model** trained using `OneVsRestClassifier`
- 📊 **Dashboard** for data analysis and model explainability (e.g., feature importance, song frequency)
- 🌐 **Streamlit Web App** to interactively input concert details and get song predictions
- 🔁 **Dynamic prediction logic**: If the new album flag is `True`, users must input 3 new songs and remove 3 of the 9 predicted ones for a final setlist

---

## 📸 App Screenshots

Dashboard
![Dashboard 1](https://github.com/user-attachments/assets/89990a68-9194-4fe0-be0e-db7150fd9bbd)

Streamlit
<img width="1601" alt="Screenshot 2025-05-23 at 15 20 53" src="https://github.com/user-attachments/assets/09a49d5d-a8eb-48ea-a3a8-157878b0ad9a" />
