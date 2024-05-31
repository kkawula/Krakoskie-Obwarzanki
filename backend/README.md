## Setup backendu

### Wirtualne środowisko

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
pip install -r requirements.txt
```

lub

```sh
make install
```

### Uruchomienie serwera

```
uvicorn main:app --reload
```

lub

```
make server
```

### Pre-commit

Aby pre-commit działał poprawnie, musisz zainstalować pre-commit.

```sh
pip install -r requirements-dev.txt
```

lub

```sh
make install-dev
```

Następnie zainstaluj pre-commit (należy to zrobić tylko raz)

```sh
pre-commit install
```

Teraz pre-commit będzie działać przed każdym commitowaniem.
