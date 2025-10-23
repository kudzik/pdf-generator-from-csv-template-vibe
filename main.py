# Importowanie potrzebnych bibliotek
import csv  # Do czytania plików CSV (Comma Separated Values)

from fpdf import FPDF  # Biblioteka do tworzenia plików PDF


def load_topics(filepath):
    """
    Funkcja do wczytywania tematów z pliku CSV

    Args:
        filepath (str): Ścieżka do pliku CSV z tematami

    Returns:
        list: Lista słowników z danymi z pliku CSV
    """
    # Otwieranie pliku CSV z odpowiednim kodowaniem UTF-8 (obsługuje polskie znaki)
    with open(filepath, newline="", encoding="utf-8") as f:
        # csv.DictReader czyta plik i zwraca każdy wiersz jako słownik
        # list() konwertuje to na listę słowników
        return list(csv.DictReader(f))


class NotebookPDF(FPDF):
    """
    Klasa dziedzicząca po FPDF do tworzenia notatnika PDF
    Zawiera niestandardowe nagłówki i stopki
    """

    def __init__(self):
        """
        Konstruktor klasy - wywołuje konstruktor klasy nadrzędnej
        i inicjalizuje zmienną topic
        """
        super().__init__()  # Wywołanie konstruktora klasy nadrzędnej (FPDF)
        self.topic = ""  # Zmienna do przechowywania aktualnego tematu
        self.current_page_topic = ""  # Temat dla aktualnie renderowanej strony
        self.page_topic = ""  # Temat zapisany w momencie renderowania strony

    def header(self):
        """
        Metoda wywoływana automatycznie na każdej stronie
        Tworzy nagłówek z nazwą tematu
        """
        # KRYTYCZNE: Zapisz temat w momencie renderowania nagłówka
        self.page_topic = self.current_page_topic

        self.set_font(
            "Arial", "B", 14
        )  # Ustawienie czcionki Arial, pogrubionej, rozmiar 14
        # cell() tworzy komórkę z tekstem
        # 0 = szerokość (0 = pełna szerokość strony)
        # 10 = wysokość
        # ln=True = przejście do nowej linii po komórce
        # align="C" = wyśrodkowanie tekstu
        # Używamy page_topic, który jest zapisany w momencie renderowania
        self.cell(0, 10, self.page_topic, ln=True, align="C")
        self.ln(10)  # Dodanie 10 punktów odstępu

    def footer(self):
        """
        Metoda wywoływana automatycznie na każdej stronie
        Tworzy stopkę z nazwą tematu (małymi literami)
        """
        self.set_y(-15)  # Ustawienie pozycji Y na 15 punktów od dołu strony
        self.set_font("Arial", "I", 10)  # Czcionka Arial, kursywa, rozmiar 10
        # Używamy page_topic, który został zapisany w header() i nie może być zmieniony
        self.cell(0, 10, self.page_topic.lower(), align="C")


def generate_notebook(topics, output_file="notebook.pdf"):
    """
    Funkcja do generowania notatnika PDF z listy tematów

    Args:
        topics (list): Lista słowników z danymi tematów
        output_file (str): Nazwa pliku wyjściowego (domyślnie "notebook.pdf")
    """
    pdf = NotebookPDF()  # Tworzenie instancji naszej klasy PDF

    # Iteracja przez każdy temat z listy
    for row in topics:
        # row["Pages"] to liczba stron dla danego tematu (konwertowana na int)
        # range() tworzy sekwencję liczb od 0 do liczby stron
        for _ in range(int(row["Pages"])):
            # WAŻNE: Ustawienie tematu PRZED dodaniem strony
            # to zapewnia, że header i footer będą miały poprawny temat
            pdf.topic = row["Topic"]  # Ustawienie aktualnego tematu
            pdf.current_page_topic = row[
                "Topic"
            ]  # Ustawienie tematu dla aktualnej strony
            print(
                f"Adding page for topic: {pdf.topic}"
            )  # Informacja o dodawanej stronie
            pdf.add_page()  # Dodanie nowej strony (automatycznie wywoła header i footer)

            # KRYTYCZNE: Nie zmieniaj current_page_topic po add_page()!
            # Pozostaw go niezmieniony do następnej iteracji

    pdf.output(output_file)  # Zapisanie pliku PDF na dysk


# Sprawdzenie czy skrypt jest uruchamiany bezpośrednio (nie importowany)
if __name__ == "__main__":
    # Wczytanie tematów z pliku CSV
    topics = load_topics("topics.csv")
    # Wygenerowanie notatnika PDF
    generate_notebook(topics)
