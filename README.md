# 📝 Flask To-Do List App

This is a simple full-stack **To-Do List** web app built using:

- **Flask** (Python)
- **Tailwind CSS** (Frontend styling)
- **SQLite** (Database)
- **SQLAlchemy** (ORM)

Users can create lists, add items with due dates, mark them complete, and save to a database or file.
![image](https://github.com/user-attachments/assets/a9d62f21-3bda-4f21-9855-476a303b5fdf)

---

## 🚀 Features

- Create editable list names  
- Add/remove to-do items  
- Set due dates  
- Toggle completion status  
- Save lists to a **SQLite DB**  
- Auto-create list if it doesn’t exist  
- Basic file-saving support coming soon  

---

## 📁 Project Structure

```plaintext
.
├── main.py             # Flask app and database logic
├── templates/
│   └── index.html      # Frontend with Tailwind + JS
├── list.db             # SQLite database file
└── README.md
```

---

## ⚙️ Requirements

- Python 3.10+
- pip

Install dependencies:

```bash
pip install flask flask_sqlalchemy flask_bootstrap flask_wtf flask_login
```

---

## 🧪 Run the App

```bash
python main.py
```

Then open your browser and visit:

```text
http://127.0.0.1:5000/
```

---

## 🛠 API

### POST `/api/lists`

Creates or updates a list by title.

**Request JSON:**

```json
{
  "title": "My List",
  "items": [
    { "text": "Buy milk", "due": "2025-04-01" },
    { "text": "Call John", "due": "2025-04-02" }
  ]
}
```

**Response:**

```json
{
  "message": "List saved successfully"
}
```

---

## 💡 Next Steps

✅ File-saving (`list_name.txt`) support  
✅ Store item completion status in DB  
⏳ User login system  
⏳ List sharing & collaboration  

---

## 🧑‍💻 Author

Built by Mathieu Adams. Inspired by the need to keep it simple, fast, and functional.

---

## 📜 License

MIT License

