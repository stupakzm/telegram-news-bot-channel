# Agent Tools & Path Reference

> **For agents:** Use the paths in this file directly. Do NOT search for tools.
>
> **If a path stops working:** Update this file before continuing, so future agents benefit from the fix.

## Python Environment

| Tool | Path | Version |
|------|------|---------|
| `python` | `C:\Users\TopAide\AppData\Local\Programs\Python\Python313\python.exe` | 3.13.1 |
| `pip` | `C:\Users\TopAide\AppData\Local\Programs\Python\Python313\Scripts\pip.exe` | 24.3.1 |
| `pytest` | `C:\Users\TopAide\AppData\Local\Programs\Python\Python313\Scripts\pytest.exe` | 8.3.4 |

## In Bash (Git Bash / MSYS2), use Windows paths like this:

```bash
/c/Users/TopAide/AppData/Local/Programs/Python/Python313/python.exe --version
/c/Users/TopAide/AppData/Local/Programs/Python/Python313/Scripts/pip.exe install -r requirements.txt
/c/Users/TopAide/AppData/Local/Programs/Python/Python313/Scripts/pytest.exe -v
```

Or use the module form (preferred, avoids PATH issues):

```bash
/c/Users/TopAide/AppData/Local/Programs/Python/Python313/python.exe -m pip install -r requirements.txt
/c/Users/TopAide/AppData/Local/Programs/Python/Python313/python.exe -m pytest -v
```

## Project Location

```
C:\Users\TopAide\projects\telegram-news-bot\
/c/Users/TopAide/projects/telegram-news-bot/   ← use this in bash commands
```

## Installed Packages

Dependencies are split:
- `requirements.txt` — production only (feedparser, google-generativeai, requests, python-dotenv)
- `requirements-dev.txt` — includes prod + pytest, pytest-mock

All packages installed into Python 3.13 site-packages at:
`C:\Users\TopAide\AppData\Local\Programs\Python\Python313\Lib\site-packages\`

## Notes

- `python` on PATH in bash resolves to `/c/msys64/mingw64/bin/python` — this is NOT the right Python. Always use the full path above.
- `pip` is not on PATH in bash — always use the full path or `-m pip`.
- `pytest` is not on PATH in bash — always use the full path or `-m pytest`.
