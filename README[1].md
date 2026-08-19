# Andrew K. Rockson — Microsoft Equity Valuation

Portfolio project featuring a gold/black equity-research frontend plus a Python FastAPI DCF engine.

## Features
- Interactive five-year DCF inputs
- Bear / Base / Bull scenarios
- Python FastAPI REST endpoint (`POST /api/dcf`)
- Automatic fair value, upside/downside and valuation signal
- Local JavaScript fallback so the demo still works when the API is offline
- Original Excel DCF/comps model included

## Run locally
1. `pip install -r requirements.txt`
2. `uvicorn app:app --reload`
3. Open `index.html` in a browser.
4. FastAPI docs: `http://127.0.0.1:8000/docs`

## Deploy
Deploy the static frontend on GitHub Pages/Netlify/Vercel and the FastAPI backend on a Python host such as Render. After deployment, change `API_BASE` near the bottom of `index.html` to the public backend URL.
