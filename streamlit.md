# 📊 Students' Social Media Addiction Analysis

[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://www.python.org/)
[![Kaggle Dataset](https://img.shields.io/badge/Data-Kaggle-orange?logo=kaggle)](https://www.kaggle.com/)

Інтерактивний дашборд для аналізу впливу соціальних мереж на життя студентів (16–25 років).  
Проект досліджує взаємозв'язок між цифровими звичками, ментальним здоров'ям та соціальними стосунками на основі даних з **6 континентів**.

---

## 🚀 Live Demo
👉 [Дивитися на Streamlit Cloud](https://social-media-addiction-final.streamlit.app/)

---

## 🌟 Ключові можливості
- 🌍 **Глобальна аналітика**: Інтерактивна карта світу (Folium) з регіональними лідерами платформ.  
- 📑 **Перевірка гіпотез**: Візуалізація впливу соцмереж на сон, навчання та конфлікти в сім'ї.  
- 🤖 **ML-Діагностика**: 3D-кластеризація користувачів (K-Means) на три сегменти: *Збалансовані*, *Група ризику*, *Залежні*.  
- 🧩 **Self-Test**: Інтерактивна форма для визначення власного цифрового профілю.  

---

## 🛠 Технологічний стек
- **Data Processing**: Python, Pandas, NumPy  
- **Visualizations**: Plotly, Folium, Seaborn  
- **Machine Learning**: Scikit-learn (K-Means Clustering)  
- **Web Framework**: Streamlit  

---

## 🔍 Головні інсайти
- 📸 **Гегемонія Instagram**: Платформа є лідером у 4 з 6 регіонів.
![Гегемонія Instagram](visuals/Insta.png)
 
- 🎵 **Алгоритмічна пастка**: Користувачі TikTok та Instagram мають найвищу залежність.
![Алгоритмічна пастка](visuals/Hypothesis_3.png)

   
- 😴 **Дефіцит сну**: Зростання часу у соцмережах безпосередньо веде до скорочення тривалості сну.  

---

## 📂 Структура репозиторію

```text
students-social-media-addiction/
├── data/
│   ├── raw/                # Вихідний набір даних (Students Social Media Addiction.csv)
│   └── processed/          # Очищений та збагачений набір (cleaned_data.csv)
│
├── notebooks/              # Покрокове дослідження в DataLab
│   └── full_analysis.ipynb
│
├── app/
│   └── streamlit_app.py     # Основний код інтерактивного додатка
│
├── visuals/                # Статичні графіки для звіту та документації (поки що пуста папка)
│   ├── 
│   ├── 
│   └── 
│
├── requirements.txt        # Перелік залежностей для середовища Streamlit
├── README.md               # Презентація проєкту
└── PROJECT_PLAN.md         # Дорожня карта (початковий план роботи)
```

---

## 🚀 Як запустити локально

### 1. Клонуйте репозиторій
```bash
git clone https://github.com/vitalii-84/Social-Media-Addiction.git
```

### 2. Встановіть залежності
```bash
pip install -r requirements.txt
```

### 3. Запустіть додаток
```bash
streamlit run app/streamlit_app.py
```

---

## 📊 Джерело даних
[Kaggle: Social Media Addiction Dataset](https://www.kaggle.com/datasets/adilshamim8/social-media-addiction-vs-relationships)






