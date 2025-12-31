# BookFlow

BookFlow is a modular library management system built with Python. It provides a clean structure for managing books, users, and borrowing operations, and is designed to be easily extendable with new features such as authentication, encryption, analytics, or modern APIs.

---

## ✨ Features

- Book management (add, remove, update)
- User and borrowing request management
- MongoDB-based data storage
- Modular and extensible architecture
- Command-line interface (CLI)
- Ready for future expansion (GUI, API, dashboards, etc.)

---

## 📦 Requirements

This project requires Python 3.8+ and a running MongoDB instance.

- Python (3.8+)
- MongoDB server
- Python dependencies listed in `requirements.txt`

Install Python dependencies into a virtual environment:

```bash
# create and activate a venv (Linux/macOS)
python -m venv BookFlowVenv
source BookFlowVenv/bin/activate

# install dependencies
pip install -r requirements.txt
```

Official MongoDB installation instructions are available here:

- MongoDB manual installation guide: https://www.mongodb.com/docs/manual/installation/

For platform-specific packages and installers (Windows, macOS, Linux), follow the link above and pick the section for your OS. If you prefer using a hosted option, see MongoDB Atlas: https://www.mongodb.com/cloud/atlas

---

## ▶️ How to Run

After installing dependencies and ensuring MongoDB is running on the default port (27017), start the CLI:

```bash
python cli.py
```

If the project needs a different MongoDB connection string (e.g., remote server or Atlas), update `db.py` accordingly.

---

## 📁 Project Structure
```text
BookFlow/
│
├── Collections/        # Data models and collections
├── services/           # Business logic and service layer
├── cli.py              # Command-line interface
├── db.py               # Database connection handler
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🛠 Planned Features

- Graphical User Interface (GUI) or API
- Data encryption

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an Issue or submit a Pull Request.
