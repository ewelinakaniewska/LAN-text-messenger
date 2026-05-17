# Komunikator Klient-Serwer (TCP/IP) 

Aplikacja sieciowa typu klient-serwer napisana w języku Python, umożliwiająca tekstową komunikację wieloosobową w czasie rzeczywistym wraz z pełnym logowaniem przebiegu rozmowy.

## Główne założenia

* **Wielowątkowość:** Serwer obsługuje każdego klienta w osobnym wątku, co pozwala na jednoczesną rozmowę wielu użytkowników.
* **Logowanie konwersacji:** Wszystkie wiadomości (wraz z IP nadawcy) oraz informacje o połączeniach i rozłączeniach są zapisywane do pliku tekstowego.
* **Niezawodność:** Transmisja danych opiera się na protokole TCP/IP, co gwarantuje poprawną kolejność i brak strat w przesyłanych wiadomościach.

## Technologie i moduły (Python 3.12.4)

Aplikacja wykorzystuje wyłącznie standardowe biblioteki Pythona:

* `socket` – realizacja niskopoziomowych połączeń sieciowych (tworzenie gniazd IPv4, nasłuchiwanie i dwukierunkowy transfer TCP).
* `threading` – zarządzanie wątkami i współbieżną obsługą wielu użytkowników.
* `select` – asynchroniczne monitorowanie wielu gniazd sieciowych jednocześnie.
* `signal` – bezpieczne przechwytywanie sygnałów systemowych (np. zamknięcie serwera przez `Ctrl+C`).
* `time` & `os` – generowanie znaczników czasu do logów oraz kontrolowane kończenie procesów.
