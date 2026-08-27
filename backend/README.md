# Backend

## Running the Backend

### 1. Go to the backend directory

```bash
cd backend
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure `.env`

Create a `.env` file inside the `backend` directory:

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=product_intelligence

JWT_SECRET_KEY=your_long_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 6. Start MongoDB

Make sure MongoDB is running locally.

### 7. Run FastAPI

```bash
uvicorn app.main:app --reload
```

### 8. Open the API

```text
http://127.0.0.1:8000
```

### 9. API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

### Quick Run

After the initial setup:

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

The backend should return:

```json
{
  "message": "Product Intelligence API",
  "status": "running"
}
```
