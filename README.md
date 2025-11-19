🇸🇪 Swedish Vocabulary Trainer — Flask App
A Flask-based web application that builds a Swedish vocabulary database from Språkbanken Karp (SALDOM) and provides live English–Swedish translations using DeepL and a local database cache.
It automatically extracts grammatical forms for nouns, verbs, adjectives, and other parts of speech and stores them in a local SQLite database.
✨ Features
🔤 1. Automatic Vocabulary Extraction
On first run, the app:
Connects to Språkbanken Karp SALDOM API
Downloads all available entries in batches
Detects part of speech (noun, verb, adjective, etc.)
Parses inflection tables to extract:
Noun forms: indefinite/definite + singular/plural
Verb forms: present, preterite, supine, imperative
Adjective forms (common, neuter, plural)
And more…
Saves all extracted words into a structured SQLite database.
🌐 2. Bidirectional Translation
Using the /dictionary route, users can:
Translate Swedish → English
Translate English → Swedish
Use DeepL only when a translation is not already stored locally
Automatically update missing translations in the database
🗄️ 3. Local SQLite Database
All vocabulary is stored inside:
se_vocabulary_db/database.db
Using Flask SQLAlchemy models for each part of speech.
🧩 4. Modular Architecture
app.py – Flask application, DB setup, initial data import
routes.py – User-facing routes
functions.py – Word extraction + translation logic
models.py – SQLAlchemy models
.env – API keys (DeepL)
📂 Project Structure
project/
│
├── app.py
├── routes.py
├── functions.py
├── models.py
├── .env
├── templates/
│   ├── main_page.html
│   └── dictionary.html
└── se_vocabulary_db/
    └── database.db   (created automatically)
🚀 Getting Started
1. Clone the repository
git clone <repo-url>
cd project
2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate     # macOS / Linux
venv\Scripts\activate        # Windows
3. Install dependencies
pip install -r requirements.txt
(If you don’t have a requirements.txt yet, I can generate one.)
4. Create a .env file
Your .env file must contain:
auth_key=YOUR_DEEPL_KEY
(You can include additional secrets here.)
5. Run the application
flask run
On first launch, the app will:
Create the se_vocabulary_db folder
Build the SQLite database
Download all word data from Språkbanken (this may take time)
🌍 API & Data Sources
🔹 Språkbanken Karp
Used for loading all Swedish words with inflection tables:
https://spraakbanken4.it.gu.se/karp/v7/query/saldom
🔹 DeepL
Used as translation fallback:
deepl.Translator(auth_key)
🔧 How Translation Works
Swedish → English
Check if baseform exists in any part-of-speech table
If translation missing:
DeepL is called
Result saved to DB
Return all grammatical forms + translation
English → Swedish
Look for an English translation match in DB
If not found:
Translate via DeepL
Normalize to lowercase
Check if Swedish result exists in DB
Save translation if found
Return appropriate forms
🛠️ Database Models
The app stores words in 8 tables:
Noun
Adjective
Verb
Adverb
ProperNoun
Numeral
Interjection
Preposition
Each with fields for English translation and grammatical forms.
🧪 Routes
/
Main page.
/dictionary
Displays translation form
Shows results from DB or DeepL
Supports direction selection (SV → EN or EN → SV)
⚠️ Notes
First startup can take several minutes because the entire SALDOM dataset (thousands of entries) is downloaded and saved.
DeepL API requires valid authentication.
.env file must not be committed to version control.
