# Python

macOS

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

Windows

```bash
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
deactivate
```

If venv does not work, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`python -m venv venv



run 

python .\xml-invoice-processor.py ./test-fatture 2017-01-01 2017-12-31

python\test-fatture