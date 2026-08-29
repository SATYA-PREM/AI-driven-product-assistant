# AI-driven-product-assistant

An AI-powered assistant that understands a user's requirements in natural language, searches the available product catalog, compares relevant products, and recommends the most suitable options.

## Running the Frontend

To start the frontend development server:

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies (first time only):
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```

## Running the Backend

To start the backend FastAPI server:

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Start the Uvicorn server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
