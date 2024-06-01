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

Możesz też ręcznie sprawdzić czy wszystko jest ok (ta sama komenda jest automatycznie wywoływana przy każdym commicie).

```sh
pre-commit run --all-files
```

#### Jak to działa?

Pre-commit sprawdza czy kod spełnia pewne wymagania przed commitowaniem. Jeśli nie spełnia, to commit nie zostanie zrobiony, ale hooki zrobią odpowiedni refactor kodu. Wprowadzone zmiany należy znowu dodać do stash i ponownie zrobić commit. Wymagania są zdefiniowane w pliku `.pre-commit-config.yaml`.

Jeśli z jakiegoś powodu chcesz zrobić commit bez sprawdzania, to możesz użyć flagi `--no-verify`.

```sh
git commit --no-verify -m "Wiadomość"
```
