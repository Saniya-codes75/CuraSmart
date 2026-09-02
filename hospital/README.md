# 🏥 CuraSmart - Smart Healthcare System

CuraSmart is a full-stack web application designed to streamline hospital management operations. It provides smart healthcare solutions like symptom checking, automated appointment booking, token generation, and ambulance tracking.

This project was developed as a professional placement project, transitioning from a lightweight SQLite architecture to a robust MySQL production database.

---

## 🚀 Key Features

* 👨‍⚕️ **Doctor Dashboard & Management**
  Manage doctor availability and appointments efficiently.

* 🎟️ **Token Generation System**
  Automatically generates unique tokens to reduce patient waiting time.

* 🚑 **Ambulance Tracking**
  Real-time ambulance status tracking for emergency response.

* 🔄 **Dynamic Database Migration**
  Smooth transition from SQLite (development) to MySQL (production).

---

## 🛠️ Tech Stack

| Layer       | Technology Used               |
| ----------- | ----------------------------- |
| Front-end   | HTML5, CSS3, JavaScript       |
| Back-end    | Python, Django Framework      |
| Database    | MySQL (Migrated from SQLite3) |
| Environment | Virtual Environment (venv)    |

---

## ⚙️ Installation & Setup Guide

Follow these steps to run the project locally:

### 1️⃣ Clone the Repository

```bash
git clone <your-repository-link-here>
cd CuraSmart
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv env
```

### 3️⃣ Activate Virtual Environment

**Windows:**

```bash
env\Scripts\activate
```

**Mac/Linux:**

```bash
source env/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Configure Database

Update your `settings.py` file with MySQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'curasnart_db',
        'USER': 'root',
        'PASSWORD': 'Kshama123@',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 6️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7️⃣ Run Server

```bash
python manage.py runserver
```

---

## 📌 Project Structure (Basic)

```
CuraSmart/
│── manage.py
│── db.sqlite3
│── requirements.txt
│
├── app/
├── templates/
├── static/
└── media/
```

---

## 🎯 Future Enhancements

* AI-based symptom prediction
* Mobile app integration
* Payment gateway integration
* Advanced analytics dashboard

---

## 🤝 Contribution

Contributions are welcome! Feel free to fork the repository and submit pull requests.

---

## 📧 Contact

* Name: Saniya ,Kshama
* Email: [saniyakhan7983841528@gmail.com](mailto:saniyakhan7983841528@gmail.com)
* Email:[kumarisham43@gmail.com](mailto:kumarisham43@gmail.com)

---
