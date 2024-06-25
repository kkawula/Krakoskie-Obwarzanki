## Setup backendu

Zalecana wersja pythona to 3.10+

### Aby uruchomić serwer wystarczy wykonać

```sh
make server
```

Komenda ta utworzy wirtualne środowisko, zainstaluje wymagane biblioteki (w tym pre-commit) i uruchomi serwer.

To samo można zrobić krok po kroku manulanie:

### Wirtualne środowisko

Najpierw utwórz wirtualne środowisko.

```sh
python -m venv venv
```

lub

```sh
python3 -m venv venv
```

Potem aktywuj wirtualne środowisko

Unix/MacOS:

```sh
source venv/bin/activate
```

Windows:

```sh
venv\Scripts\activate
```

### Instalacja bibliotek

```sh
make install
```

lub

```sh
pip install -r requirements.txt
```

dla developera

```sh
make install-dev
```

lub

```sh
pip install -r requirements-dev.txt
pre-commit install
```

### Uruchomienie serwera

```
make server
```

lub

```
python3 app/main.py
```

### Pre-commit

Pre-commit będzie działać przed każdym commitowaniem.

Komenda `pre-commit run` sprawdza tylko zmienione pliki, które zostały dodane do staged (`git add .`) (automatycznie wywoływana przy każdym commicie), natomiast po dodaniu flagi `--all-files` sprawdza wszystkie pliki.

Do tych komend utworzone są skróty w Makefile:

```sh
make pre-commit
```

```sh
make pre-commit-all
```

#### Jak to działa?

Pre-commit sprawdza czy kod spełnia pewne wymagania przed commitowaniem. Jeśli nie spełnia, to commit nie zostanie wykonany, ale hooki zrobią odpowiedni refactor kodu (w wiekszości przypadków). Wprowadzone zmiany należy znowu dodać do staged i ponownie zrobić commit. Wymagania są zdefiniowane w pliku `.pre-commit-config.yaml`.

Jeśli z jakiegoś powodu chcesz zrobić commit bez sprawdzania, to możesz użyć flagi `--no-verify`.

```sh
git commit --no-verify -m "Wiadomość"
```
