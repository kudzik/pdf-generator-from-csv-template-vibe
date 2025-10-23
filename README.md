# Generator Notatnika PDF

Program do automatycznego generowania notatnika PDF z tematów wczytanych z pliku CSV.

## 🚀 Funkcjonalności

- **Automatyczne generowanie PDF** z tematów z pliku CSV
- **Spójne nagłówki i stopki** na każdej stronie
- **Elastyczna liczba stron** dla każdego tematu
- **Obsługa polskich znaków** (UTF-8)
- **Szczegółowe komunikaty** o postępie generowania
- **Obsługa błędów** z informatywnymi komunikatami

## 📋 Wymagania

- Python 3.7+
- Biblioteka `fpdf2`

## 🛠️ Instalacja

1. **Sklonuj repozytorium:**
   ```bash
   git clone <repository-url>
   cd pdf-generator
   ```

2. **Utwórz środowisko wirtualne:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # lub
   .venv\Scripts\activate  # Windows
   ```

3. **Zainstaluj zależności:**
   ```bash
   pip install fpdf2
   ```

## 📁 Struktura plików

```
pdf-generator/
├── main.py          # Główny skrypt
├── topics.csv        # Plik z tematami
├── notebook.pdf       # Wygenerowany notatnik
├── .venv/           # Środowisko wirtualne
└── README.md        # Ta dokumentacja
```

## 📊 Format pliku CSV

Plik `topics.csv` powinien mieć następującą strukturę:

```csv
Order,Topic,Pages
1,Variables,2
2,Lists,3
3,Functions,3
```

### Kolumny:
- **Order**: Kolejność tematu (opcjonalne)
- **Topic**: Nazwa tematu (wyświetlana w nagłówku i stopce)
- **Pages**: Liczba stron dla danego tematu

## 🎯 Użycie

### Podstawowe uruchomienie:
```bash
python main.py
```

### Programowe użycie:
```python
from main import load_topics_from_csv, generate_notebook_pdf

# Wczytaj tematy
topics = load_topics_from_csv("topics.csv")

# Wygeneruj notatnik
generate_notebook_pdf(topics, "moj_notatnik.pdf")
```

## 🏗️ Architektura kodu

### Główne komponenty:

1. **`load_topics_from_csv()`** - Wczytuje dane z pliku CSV
2. **`NotebookPDF`** - Klasa do generowania PDF z niestandardowymi nagłówkami/stopkami
3. **`generate_notebook_pdf()`** - Główna funkcja generująca notatnik
4. **`main()`** - Punkt wejścia programu

### Zasady projektowe:

- **Single Responsibility**: Każda funkcja ma jedną odpowiedzialność
- **Type Hints**: Wszystkie funkcje mają adnotacje typów
- **Error Handling**: Obsługa błędów z informatywnymi komunikatami
- **Constants**: Stałe konfiguracyjne w klasie
- **Documentation**: Szczegółowe docstringi

## 🔧 Konfiguracja

Możesz dostosować wygląd PDF modyfikując stałe w klasie `NotebookPDF`:

```python
class NotebookPDF(FPDF):
    # Czcionka nagłówka
    HEADER_FONT = ("Arial", "B", 14)
    
    # Czcionka stopki  
    FOOTER_FONT = ("Arial", "I", 10)
    
    # Wysokości elementów
    HEADER_HEIGHT = 10
    FOOTER_HEIGHT = 10
    
    # Pozycjonowanie
    FOOTER_Y_POSITION = -15
    LINE_SPACING = 10
```

## 🐛 Rozwiązywanie problemów

### Błąd: "Nie można znaleźć pliku: topics.csv"
- Sprawdź czy plik `topics.csv` istnieje w tym samym katalogu co `main.py`

### Błąd: "Błąd podczas czytania pliku CSV"
- Sprawdź format pliku CSV
- Upewnij się, że plik ma nagłówki: `Topic,Pages`

### Błąd: "Lista tematów nie może być pusta"
- Sprawdź czy plik CSV nie jest pusty
- Sprawdź czy plik ma poprawne dane

## 📝 Przykład użycia

1. **Przygotuj plik CSV:**
   ```csv
   Topic,Pages
   Wprowadzenie do Pythona,3
   Zmienne i typy danych,2
   Pętle i warunki,4
   ```

2. **Uruchom generator:**
   ```bash
   python main.py
   ```

3. **Sprawdź wynik:**
   - Plik `notebook.pdf` zostanie utworzony
   - Każda strona będzie miała spójny nagłówek i stopkę

## 🤝 Wkład w rozwój

1. Fork repozytorium
2. Utwórz branch dla nowej funkcjonalności
3. Wprowadź zmiany
4. Dodaj testy
5. Utwórz Pull Request

## 📄 Licencja

Ten projekt jest dostępny na licencji MIT.

## 👨‍💻 Autor

Artur Kud 2025
