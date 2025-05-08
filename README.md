Job Market Data Engineering Project -

This project aims to scrape, clean, standardize, and enrich job listing data from multiple sources such as Naukri, LinkedIn, Monster, and others. The goal is to build a structured dataset for exploratory analysis, dashboards, or feeding into ML pipelines.

✅ Key Features Implemented So Far
🔍 Web Scraping
Scraped job listings from multiple job portals (Naukri, LinkedIn, Monster, etc.).

Parsed job title, company, location, experience, and other fields.

Handled edge cases like missing or malformed data, multiple locations, etc.

🧹 Data Cleaning & Preprocessing
Cleaned and standardized job titles and experience strings.

Extracted structured experience ranges (min, max years).

Removed non-relevant scraped text artifacts.

Normalized company names (partial logic to handle typos, misformats).

🏙️ Location Extraction
Built a robust logic to extract city, state, and country from messy location strings.

Managed entries with multiple cities or "remote" indicators.

Utilized a cities.json file with a structured city-to-state mapping.

Standardized city spellings (e.g., “bengluru” → “bengaluru”, “gurgaon” → “gurugram”).

🧾 Experience & Industry Categorization
Parsed experience level from job title and/or metadata.

Categorized jobs into experience buckets (Fresher, Junior, Mid, Senior).

Inferred industry sector from job title or company sector.

🆔 Unique Job ID Generation
Implemented a persistent job ID system per source.

Format: e.g., TAL0001, MON0002.

Maintained counters using a job_id_counter.json.

🧠 Flexible Structure
Designed code to be modular and extensible.

Used external config/mapping files where needed (cities.json, job title keywords, etc.).

Plan to expand with deduplication, ML-based matching, and dashboarding.

🔧 Tech Stack
Python 3.10+

BeautifulSoup, requests for scraping

pandas for data processing

json, os, re, sys for file and text handling