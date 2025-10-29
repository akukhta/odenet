# Create python virtual environment (venv) and install dependencies
IF NOT EXIST ".venv" (
    python3.7 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
)

source .venv/bin/activate
REM Do not forget Ctrl+C the terminal once you are done
jupyter lab "OdeNetAccess.ipynb"
pause

# Deactiavate venv
deactivate