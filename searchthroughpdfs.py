import PyPDF2
import tkinter as tk
from tkinter.filedialog import askopenfilenames
import pyperclip
import os

def search_in_pdfs():
    # Setup des Tkinter-Fensters
    root = tk.Tk()
    root.withdraw()  # Wir möchten nicht das gesamte Tk-Fenster sehen

    # Dateiauswahldialog
    file_paths = askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if not file_paths:
        print("No files selected.")
        return

    # Eingabe des zu suchenden Strings
    search_string = input("Enter the string to search for: ")

    # Vorbereiten der Ergebnisdatei
    results = []
    base_dir = os.path.dirname(file_paths[0])  # Annahme, dass alle Dateien im selben Verzeichnis sind

    # Durchlaufen der ausgewählten Dateien
    for pdf_path in file_paths:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            print(f"Searching in {pdf_path}...")

            # Suche nach dem String in jeder Seite
            found = False
            for page_number, page in enumerate(pdf_reader.pages, start=1):
                text = page.extract_text()
                if search_string in text:
                    results.append(f'String "{search_string}" found in {os.path.basename(pdf_path)} on page {page_number}')
                    pyperclip.copy(pdf_path)  # Kopieren des Dateipfads in die Zwischenablage
                    found = True

    # Schreiben der Ergebnisse in eine Datei
    with open(os.path.join(base_dir, 'found.txt'), 'w') as result_file:
        for result in results:
            result_file.write(result + '\n')

    print(f"Results saved in {os.path.join(base_dir, 'found.txt')}")

if __name__ == "__main__":
    search_in_pdfs()
