# Local Setup

## Prerequisites

- Python 3.11+
- PostgreSQL 17.5+
- dbmate 2.27+

## 1. Clone the repository

```bash
git clone https://github.com/WojtekKozieja/marketplace-api.git
cd marketplace-api
```

## 2. Create database

Open PostgreSQL and create the database:

```sql
CREATE DATABASE marketplace;
```

## 3. Set up environment variables

```bash
cp .env.example .env
```

Edit '.env' with your database credentials

## 4. Create virtual environment + install dependencies

```bash
python -m venv venv
source venv/Scripts/activate

pip install -r requirements.txt
```

## 5. Run migrations

Run migrations in each folder:

```bash
cd database
dbmate -d . -u <DATABASE_URL>?sslmode=disable up

cd triggers
dbmate -d . -u <DATABASE_URL>?sslmode=disable up
```

Optionally — load test data:

*firstly you must insert test users in python but before you do it you must start uvicron:*
start uvicorn:
```bash
cd ../../app
uvicorn main:app --reload
```

insert test users (in new terminal):

```bash
cd marketplace-api/app/test_inserts
python insert_users.py  #this may take a while due to password hashing
```

Run migrations in test_inserts folder:
```bash
cd ../../database/test_inserts
dbmate -d . -u <DATABASE_URL>?sslmode=disable up
```

## 6. Start the server
*If you loaded test data in step 5, the server is already running*
```bash
cd ../../app
uvicorn main:app --reload
```

API will be available at: [http://localhost:8000/docs](http://localhost:8000/docs)