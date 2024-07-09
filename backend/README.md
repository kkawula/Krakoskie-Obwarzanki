## Setup backendu za pomocą Makefile (zalecana zainstalowana wersja pythona 3.10+)

Aby sprawdzić wersję pythona, wpisz w terminalu:

```sh
python3 --version
```

powinno zwrócić coś w stylu `Python 3.1x.x`

### Zmienne środowiskowe

- Pierwszym krokiem jest uzupełnienie odpowiednich zmiennych środowiskowych oraz zmiana pliku `.env.example` na `.env`

### Pobranie wymaganych bibliotek

```sh
make server
```

Komenda ta utworzy wirtualne środowisko, zainstaluje wymagane biblioteki, aby uruchomić serwer.

### Wersja developerska

Jeśli nigdy wcześniej nie korzystałeś z hooków przed commitami, prawdopodobnie trzeba będzie wykonać poniższą komendę, aby pre-commit działał poprawnie:

```sh
git config --unset-all core.hooksPath
```

W celu wprowadzenia zmian zaleca się doinstalowanie biblioteki `pre-commit` w tym celu należy wykonać

```sh
make dev
```

Niestety środowisko aktywowane jest tylko w ramach jednej sesji terminala, w tym przypadku wykonania make. Aby korzystać z np. `pre-commit run` trzeba aktywować środowisko ręcznie.

```sh
source venv/bin/activate
```

## Setup backendu ręcznie

To samo można zrobić krok po kroku manualnie:

### Wirtualne środowisko

Najpierw utwórz wirtualne środowisko.

```sh
python3 -m venv venv
```

Aktywuj wirtualne środowisko

```sh
source venv/bin/activate
```

### Instalacja bibliotek

wymagane biblioteki

```sh
pip install -r requirements.txt
```

biblioteki do developmentu

```sh
pip install -r requirements-dev.txt
pre-commit install
```

## Uruchomienie serwera

```
make server
```

lub

```
python3 app/main.py
```

## Pre-commit

Po zainstalowaniu komendą `pre-commit install` pre-commit będzie działał przed każdą próbą commita.

Komenda `pre-commit run` sprawdza tylko zmienione pliki, które zostały dodane do staged (`git add .`) (automatycznie wywoływana przy każdym commicie), natomiast po dodaniu flagi `--all-files` sprawdza wszystkie pliki.

Do tych komend utworzone są skróty w Makefile:

```sh
make pre-commit
```

```sh
make pre-commit-all
```

### Jak to działa?

Pre-commit sprawdza czy kod spełnia pewne wymagania przed commitowaniem. Jeśli nie spełnia, to commit nie zostanie wykonany, ale hooki zrobią odpowiedni refactor kodu (w wiekszości przypadków). Wprowadzone zmiany należy znowu dodać do staged i ponownie zrobić commit. Wymagania są zdefiniowane w pliku `.pre-commit-config.yaml`.

Jeśli z jakiegoś powodu chcesz zrobić commit bez sprawdzania, to możesz użyć flagi `--no-verify`.

```sh
git commit --no-verify -m "Wiadomość"
```

