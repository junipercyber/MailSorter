# MailSorter

A Python tool for automatically sorting emails based on configurable rules.

## Features
- Connect to email accounts via IMAP (SSL)
- Rule-based email classification
- Keyword and sender pattern matching
- CLI interface with dry-run mode
- Configurable sorting rules via JSON

## Installation
```bash
git clone <repo-url>
cd MailSorter
cp config.json.example config.json
# Edit config.json with your email credentials
```

## Usage

### Test connection
```bash
python main.py --test
```

### Sort emails (dry run)
```bash
python main.py --sort --limit 20
```

### Sort emails (actual)
```bash
python main.py --sort --no-dry-run
```

## Configuration
Edit `config.json` to add your email credentials and sorting rules. See `config.json.example` for reference.