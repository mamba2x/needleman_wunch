# Needleman-Wunsch Alignment Web App

A small Python website that runs the Needleman-Wunsch global sequence alignment algorithm.

## Features

- Enter two DNA, RNA, or protein sequences
- Adjust match, mismatch, and gap scores
- View the best global alignment
- View the final alignment score
- View the full score matrix

## Run the Website

```powershell
python .\web_app.py
```

Then open:

```text
http://127.0.0.1:8765
```

## Run the Command Line Version

```powershell
python .\needleman_wunsch.py
```

## Files

- `needleman_wunsch.py` contains the alignment algorithm.
- `web_app.py` contains the Python web server and website interface.

