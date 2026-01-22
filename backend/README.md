# Flask Backend

A Flask backend API for seaweed quality control analysis, powered by SQLite and Google Gemini.

## Prerequisites

### Install SQLite
SQLite is required for local data persistence.

- **macOS**: Usually pre-installed. To update: `brew install sqlite`
- **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install sqlite3`
- **Windows**: Download from [sqlite.org](https://www.sqlite.org/download.html) or use `choco install sqlite`

### Google Gemini API Key
This application uses Gemini 2.5 Flash for seaweed analysis. You must have a valid API key.

1.  Go to [Google AI Studio](https://aistudio.google.com/).
2.  Generate a new API key.
3.  Add it to your `.env` file as shown in the [Setup](#setup) section.

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create and configure your `.env` file:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

5. Initialize and seed the database:
```bash
python seed_db.py
```

## Running the Application

```bash
python app.py
```

The server will start on `http://localhost:5001`.

## Available Endpoints

- `GET /api/batches` - Get all batches
- `GET /api/batch/<id>` - Get batch details
- `GET /api/batch/<id>/qc-records` - Get QC records for a batch
- `POST /api/analyze-qc-image` - Run AI analysis on an image/video
- `PUT /api/qc-record/<id>` - Update an existing QC record
- `GET /api/uploads/<filename>` - Serve uploaded media
