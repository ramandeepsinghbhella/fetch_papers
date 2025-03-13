# Fetch Research Papers 📚  
A Python CLI tool to fetch research papers from PubMed based on a given query and save the results as a CSV file.  

---

## 📌 Features  
- Fetches research papers based on a search query.  
- Saves results to a `.csv` file (or prints to the console).  
- Supports command-line arguments for better control.  
- Provides a debug mode for detailed output.  
- Handles edge cases like missing queries or incorrect file extensions.  

---

## 🛠 Installation  

### 1. Clone the Repository  
```sh
git clone https://github.com/ramandeepsinghbhella/fetch_papers.git
cd fetch-papers
```

### 2. Check python version (>=3.13)
```sh
python --version
```
if python version not statisfied download required python version (>=3.13) and use
```sh
poetry env use python3.13
```
---


### 3. Install Dependencies Using Poetry
```sh
poetry install
```
---

## 🚀 Usage Guide

### Basic usage
```sh
poetry run python src/fetch_research_papers/fetch_papers_cli.py "cancer research"
```

### Save Results to a CSV File
```sh
poetry run python src/fetch_research_papers/fetch_papers_cli.py "cancer research" -f results.csv
```

### Enable debug mode
```sh
poetry run python src/fetch_research_papers/fetch_papers_cli.py "cancer research" -d
```
### Show help
```sh
poetry run python src/fetch_research_papers/fetch_papers_cli.py "cancer research" -h
```
### List all fetched research papers
```sh
poetry run python src/fetch_research_papers/get_papers_list.py
```
