<h1 align = "center">🏏 Rohit Sharma Career Scraper </h1>

A Python-based web scraping project to collect all of Rohit Sharma's batting scores in international cricket since his senior debut. The data is fetched from [ESPNcricinfo](https://www.espncricinfo.com/) using BeautifulSoup and stored in CSV/Parquet formats using Pandas.

---

## 📌 Project Objective

The aim of this project is to:
- Scrape detailed batting scorecards of Rohit Sharma for every match he has played
- Store and organize the data for further analysis or visualization
- Provide a clean and reproducible codebase for cricket data enthusiasts

---

## 🚀 Features

- Scrapes match-wise batting scores for Rohit Sharma
- Supports all international (Test, ODI, T20i) as well as domestic (IPL, Ranji Trophy) formats
- Outputs data in both `.csv` and `.parquet` formats
- Clean modular code for easy extension
- Minimal and easy-to-follow dependencies

## 🛠️ Tech Stack

- **Python 3.8+**
- **BeautifulSoup** – for HTML parsing
- **Requests** – for making HTTP requests
- **Pandas** – for data storage and manipulation
- **Jupyter Notebook (optional)** – for quick analysis
- **PyTest** - For unit testing

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/rohit-innings-scraper.git
   cd rohit-innings-scraper
   ```
2. **Create a virtual environment (Optional)**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  
    # On Windows: .venv\Scripts\activate
    ```
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the scrapper**
    ```bash
    python main.py --fileformat <'csv' or 'parquet'>
    ```
---
## 📊 Expected Output


---
## 🤝 Contributing
Pull requests are welcome!  
For major changes, please open an issue first to discuss what you would like to change or improve.

---

## 📜 License
This project is open-source and available under the [MIT License](/LICENSE).

---

## 📬 Contact
Created with 💙 by [Mohmmed Owais Khan](https://github.com/mohammedOwaiskh)  
For any suggestions or queries, feel free to reach out!

---