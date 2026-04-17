# Marketplace API

🌐 **Live API:** [marketplace-api](http://3.236.245.192:8000/docs)

A full-featured online marketplace platform built with FastAPI and PostgreSQL, featuring advanced database partitioning, triggers, and real-time offer management.

## ✨ Features

- **User Management**: Registration, authentication with bcrypt password hashing
- **Product Listings**: Create, update, and search offers across multiple categories
- **Order Processing**: Complete order workflow with inventory management
- **Favorites System**: Users can save and remove favorite offers
- **Price History**: Automatic tracking of price changes
- **Smart Partitioning**: Optimized database performance through strategic partitioning
- **Auto-Deactivation**: Cron job to automatically deactivate expired offers

## 🛠 Tech Stack

- **Backend Framework**: FastAPI 0.135.1
- **Language**: Python 3.11.8
- **Database**: PostgreSQL 17.5 with SQLAlchemy 2.0.48
- **Authentication**: bcrypt 5.0.0, JWT Tokens (python-jose 3.5.0)
- **Task Scheduling**: APScheduler 3.11.2
- **Server**: Uvicorn 0.42.0
- **Deployment**: AWS EC2
- **Data Validation**: Pydantic 2.12.5

## 🗄 Database Architecture

### Partitioning Strategy

The database implements three types of partitioning for optimal performance:

#### 1. **List Partitioning** (Offers)
- Partitioned by `is_active` status
- `active_offers`: Currently available offers
- `inactive_offers`: Expired or sold-out offers
- **Benefit**: Faster queries on active offers with partition pruning

#### 2. **Range Partitioning** (Orders & Order Details)
- Partitioned by `order_date` (yearly partitions)
- Partitions: 2024, 2025, 2026
- **Benefit**: Efficient historical data queries and archival

#### 3. **Hash Partitioning** (Favourites)
- Partitioned by `user_id` (4 partitions using modulus)
- **Benefit**: Evenly distributed load across partitions

### Database Triggers

Four automated triggers handle business logic:

1. **Order Details Snapshot** (`trg_snapshot_order_details`)
   - Captures offer details at purchase time
   - Ensures historical accuracy even if offer is modified

2. **Price Logging** (`trg_price_logs`)
   - Automatically logs all price changes
   - Tracks price history for analytics

3. **Inventory Management** (`trg_offers_quantity`)
   - Auto-decrements offer quantity on purchase
   - Auto-deactivates offers when quantity reaches zero

4. **Favourites Cleanup** (`trg_del_inactive_offers`)
   - Prevents users from favoriting inactive offers
   - Maintains data integrity

## 📁 Project Structure

```
marketplace-api/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── scheduled_deactivate_offers.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── category.py
│   │   ├── favourite.py
│   │   ├── my_offer.py
│   │   ├── offer.py
│   │   ├── order.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── category.py
│   │   ├── favourites.py
│   │   ├── offer.py
│   │   ├── order.py
│   │   ├── price_log.py
│   │   └── user.py
│   │
│   └── test_inserts/
│       └── insert_users.py
│
├── database/
│   ├── 1_Create_Users.sql
│   ├── 2_Create_Categories.sql
│   ├── 3_Create_Offers.sql
│   ├── 4_Create_Orders.sql
│   ├── 5_Create_Order_Details.sql
│   ├── 6_Create_Price_Logs.sql
│   ├── 7_Create_Favourites.sql
│   ├
│   ├── test_inserts/
│   │   ├── 92_Insert_Categories.sql
│   │   ├── 93_Insert_Offers.sql
│   │   ├── 94_Insert_Orders.sql
│   │   ├── 95_Insert_Favourities.sql
│   │   └── 96_Insert_Order_Details.sql
│   ├
│   └── triggers/
│       ├── 11_Trigger_Order_Details.sql
│       ├── 12_Trigger_Price_Logs.sql
│       ├── 13_Trigger_Offers_Quantity.sql
│       └── 14_Trigger_Favourites.sql
│
├── Readme.md
├── requirements.txt
├── .env.example
└── .gitignore
```


## 📡 API Endpoints
🔒 — requires Bearer JWT token

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/token` | Login — returns JWT access token |

&nbsp;

### Users (`/users`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/users` | Get all users (paginated) |
| GET    | `/users/me` | Get current user 🔒 |
| POST   | `/users` | Register new user |

**Password Security**

- Passwords hashed using bcrypt with salt
- Maximum password length: 72 characters
- Authentication via JWT token (Bearer, expires in 30 min)

&nbsp;

### Categories (`/categories`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/categories` | Get all categories |
| GET    | `/categories/{category_id}` | Get category by ID |
| GET    | `/categories/{category_id}/subcategories` | Get subcategories |

&nbsp;

### Offers (`/offers`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/offers` | Get offers (filterable by `category_id`, `subcategory_id`, `min_price`, `max_price`, `is_active`) |
| GET    | `/offers/{offer_id}` | Get offer by ID |
| GET    | `/offers/{offer_id}/price_logs` | Get price history for an offer |

&nbsp;

### My Offers (`/users/me/offers`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/users/me/offers` | Get current user's offers 🔒 |
| POST   | `/users/me/offers` | Create new offer 🔒 |
| PATCH  | `/users/me/offers/{offer_id}` | Update offer 🔒 |
| PATCH  | `/users/me/offers/{offer_id}/end-date` | Extend offer end date 🔒 |

&nbsp;

### Favourites (`/users/me/favourites`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/users/me/favourites` | Get current user's favourite offers 🔒 |
| POST   | `/users/me/favourites/{offer_id}` | Add offer to favourites 🔒 |
| DELETE | `/users/me/favourites/{offer_id}` | Remove offer from favourites 🔒 |

&nbsp;

### Orders (`/users/me/orders`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/users/me/orders` | Get current user's orders 🔒 |
| GET    | `/users/me/orders/{order_id}` | Get order by ID 🔒 |
| GET    | `/users/me/orders/{order_id}/order_details` | Get order details 🔒 |
| POST   | `/users/me/orders` | Create new order 🔒 |