# Introduction

# Setup and Build
## Creating the virtual environment
### Windows
1. In cmd, create the environment
```
python -m venv .venv
```
2. Activate the environment
```
.venv\Scripts\activate.bat
```
3. Install dependencies
```
pip install -r requirements.txt
```
### Mac/Linux
1. In terminal, create the environment
```
python3 -m venv .venv
```
2. Activate the environment
```
source .venv/bin/activate
```
3. Install dependencies
```
pip install -r requirements.txt
```
## Adding libraries through pip
Run the following command after using pip install if the library is needed for the project
```
pip freeze > requirements.txt
```