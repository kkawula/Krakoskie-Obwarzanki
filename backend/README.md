## Setup backendu

### Wirtualne środowisko

Najpierw utwórz wirtualne środowisko. Możesz to zrobić za pomocą Makefile. Komenda ta utworzy wirtualne środowisko w folderze `venv`, następnie je aktywuje i zainstaluje wymagane biblioteki. Po wykonaniu tej komendy, można już [wystartować server](#uruchomienie-serwera).

```sh
make venv
```

lub ręcznie

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

### Uruchomienie serwera

```
make server
```

lub

```
python app/main.py
```

### Pre-commit

Aby pre-commit działał poprawnie, musisz zainstalować pre-commit. (jeśli środowisko wirtualne utworzyłeś za pomocą Makefile, to pre-commit jest już zainstalowany)

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

Możesz też ręcznie sprawdzić czy wszystko jest ok (ta sama komenda jest automatycznie wywoływana przy każdym commicie). `pre-commit run` sprawdza tylko zmienione pliki, które zostały dodane do staged (`git add .`), a `pre-commit run --all-files` sprawdza wszystkie pliki.

```sh
pre-commit run
```

```sh
pre-commit run --all-files
```

#### Jak to działa?

Pre-commit sprawdza czy kod spełnia pewne wymagania przed commitowaniem. Jeśli nie spełnia, to commit nie zostanie zrobiony, ale hooki zrobią odpowiedni refactor kodu. Wprowadzone zmiany należy znowu dodać do stash i ponownie zrobić commit. Wymagania są zdefiniowane w pliku `.pre-commit-config.yaml`.

Jeśli z jakiegoś powodu chcesz zrobić commit bez sprawdzania, to możesz użyć flagi `--no-verify`.

```sh
git commit --no-verify -m "Wiadomość"
```
