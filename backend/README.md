## How to setup

### First create a virtual environment with

```sh
python -m venv venv
```

or

```sh
python3 -m venv venv
```

### Then activate the virtual environment with

On Windows

```sh
venv\Scripts\activate
```

On Unix or MacOS

```sh
source venv/bin/activate
```

### Then install the dependencies with

```sh
pip install -r requirements.txt
```

## Finally run app with

```
uvicorn main:app --reload
```
