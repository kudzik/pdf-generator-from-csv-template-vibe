#!/usr/bin/env python3
"""
Generator notatnika PDF z tematów z pliku CSV

Ten skrypt generuje notatnik PDF z tematów wczytanych z pliku CSV.
Każdy temat może mieć różną liczbę stron, a każda strona ma spójny
nagłówek i stopkę z nazwą tematu.

Autor: Artur Kud
Data: 2025
"""

import csv
from typing import Dict, List

from fpdf import FPDF


def load_topics_from_csv(filepath: str) -> List[Dict[str, str]]:
    """
    Wczytuje tematy z pliku CSV.

    Args:
        filepath: Ścieżka do pliku CSV z tematami

    Returns:
        Lista słowników z danymi tematów (Topic, Pages)

    Raises:
        FileNotFoundError: Jeśli plik nie istnieje
        csv.Error: Jeśli plik CSV jest uszkodzony
    """
    try:
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(
                file
            )  # czyta plik i zwraca każdy wiersz jako słownik
            return list(reader)
    except FileNotFoundError:
        raise FileNotFoundError(f"Nie można znaleźć pliku: {filepath}")
    except Exception as e:
        raise csv.Error(f"Błąd podczas czytania pliku CSV: {e}")


class NotebookPDF(FPDF):
    """
    Klasa do tworzenia notatnika PDF z niestandardowymi nagłówkami i stopkami.

    Dziedziczy po FPDF i dodaje funkcjonalność automatycznego
    generowania nagłówków i stopek dla każdej strony.
    """

    # Stałe konfiguracyjne
    HEADER_FONT = ("Arial", "B", 14)
    FOOTER_FONT = ("Arial", "I", 10)
    HEADER_HEIGHT = 10
    FOOTER_HEIGHT = 10
    FOOTER_Y_POSITION = -15
    LINE_SPACING = 10

    def __init__(self):
        """
        Inicjalizuje notatnik PDF.

        Ustawia podstawowe parametry i inicjalizuje zmienne
        do przechowywania informacji o aktualnym temacie.
        """
        super().__init__()
        self._current_topic = ""  # aktualny temat
        self._page_topic = ""  # temat dla aktualnej strony

    def set_topic(self, topic: str) -> None:
        """
        Ustawia temat dla aktualnej strony.

        Args:
            topic: Nazwa tematu do wyświetlenia w nagłówku i stopce
        """
        self._current_topic = topic

    def header(self) -> None:
        """
        Generuje nagłówek strony.

        Automatycznie wywoływana przez FPDF przy dodawaniu nowej strony.
        Wyświetla nazwę tematu w nagłówku strony i rysuje poziome linie.
        """
        # Zapisz temat w momencie renderowania nagłówka
        # to zapewnia spójność z stopką
        self._page_topic = self._current_topic

        # Ustaw czcionkę i wyświetl nagłówek
        self.set_font(*self.HEADER_FONT)
        self.cell(w=0, h=self.HEADER_HEIGHT, txt=self._page_topic, ln=True, align="C")

        # Rysuj linię pod nagłówkiem
        self.line(10, self.get_y(), 200, self.get_y())

        self.ln(self.LINE_SPACING)

        # Dodaj dodatkowe linie pomocnicze dla notowania
        self._add_notebook_lines()

    def footer(self) -> None:
        """
        Generuje stopkę strony.

        Automatycznie wywoływana przez FPDF przy dodawaniu nowej strony.
        Wyświetla nazwę tematu małymi literami w stopce strony i rysuje linię.
        """
        # Rysuj linię nad stopką
        self.line(10, self.FOOTER_Y_POSITION - 5, 200, self.FOOTER_Y_POSITION - 5)

        # Ustaw pozycję i czcionkę
        self.set_y(self.FOOTER_Y_POSITION)
        self.set_font(*self.FOOTER_FONT)

        # Wyświetl stopkę z tematem małymi literami
        self.cell(w=0, h=self.FOOTER_HEIGHT, txt=self._page_topic.lower(), align="C")

    def _add_notebook_lines(self) -> None:
        """
        Dodaje poziome linie pomocnicze na stronie ułatwiające notowanie.

        Rysuje linie w regularnych odstępach na całej stronie.
        """
        # Oblicz dostępną wysokość strony (bez nagłówka i stopki)
        page_height = 297  # A4 height in mm
        margin_top = self.get_y()
        margin_bottom = 20  # miejsce na stopkę

        # Rysuj linie co 7mm (odpowiada standardowemu odstępowi w zeszytach)
        line_spacing = 7
        current_y = margin_top + line_spacing

        while current_y < page_height - margin_bottom:
            self.line(10, current_y, 200, current_y)
            current_y += line_spacing


def create_pages_for_topic(pdf: NotebookPDF, topic: str, page_count: int) -> None:
    """
    Tworzy określoną liczbę stron dla danego tematu.

    Args:
        pdf: Instancja NotebookPDF
        topic: Nazwa tematu
        page_count: Liczba stron do utworzenia
    """
    for page_num in range(page_count):
        pdf.set_topic(topic)
        # print(f"Dodawanie strony {page_num + 1} dla tematu: {topic}")
        pdf.add_page()


def generate_notebook_pdf(
    topics: List[Dict[str, str]], output_file: str = "notebook.pdf"
) -> None:
    """
    Generuje notatnik PDF z listy tematów.

    Args:
        topics: Lista słowników z danymi tematów
        output_file: Nazwa pliku wyjściowego

    Raises:
        ValueError: Jeśli lista tematów jest pusta
        KeyError: Jeśli brakuje wymaganych kluczy w danych
    """
    if not topics:
        raise ValueError("Lista tematów nie może być pusta")

    # Sprawdź czy wszystkie wymagane klucze są obecne
    required_keys = ["Topic", "Pages"]
    for i, topic_data in enumerate(topics):
        for key in required_keys:
            if key not in topic_data:
                raise KeyError(f"Brakuje klucza '{key}' w temacie {i + 1}")

    # Utwórz instancję PDF
    pdf = NotebookPDF()

    # Generuj strony dla każdego tematu
    for topic_data in topics:
        topic_name = topic_data["Topic"]
        page_count = int(topic_data["Pages"])

        create_pages_for_topic(pdf, topic_name, page_count)

    # Zapisz plik PDF
    try:
        pdf.output(output_file)
        print(f"Notatnik PDF został zapisany jako: {output_file}")
    except Exception as e:
        raise RuntimeError(f"Błąd podczas zapisywania pliku PDF: {e}")


def main() -> None:
    """
    Główna funkcja programu.

    Wczytuje tematy z pliku CSV i generuje notatnik PDF.
    """
    try:
        # Wczytaj tematy z pliku CSV
        print("Wczytywanie tematów z pliku CSV...")
        topics = load_topics_from_csv("topics.csv")
        print(f"Wczytano {len(topics)} tematów")

        # Wygeneruj notatnik PDF
        print("Generowanie notatnika PDF...")
        generate_notebook_pdf(topics)

        print("✅ Notatnik PDF został pomyślnie wygenerowany!")

    except FileNotFoundError as e:
        print(f"❌ Błąd: {e}")
        print("Sprawdź czy plik 'topics.csv' istnieje w bieżącym katalogu.")

    except csv.Error as e:
        print(f"❌ Błąd pliku CSV: {e}")
        print("Sprawdź format pliku CSV.")

    except (ValueError, KeyError) as e:
        print(f"❌ Błąd danych: {e}")
        print("Sprawdź zawartość pliku CSV.")

    except Exception as e:
        print(f"❌ Nieoczekiwany błąd: {e}")


if __name__ == "__main__":
    main()
