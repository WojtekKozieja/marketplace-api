# Marketplace API

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
- **Database**: PostgreSQL with SQLAlchemy 2.0.48
- **Authentication**: bcrypt 5.0.0
- **Task Scheduling**: APScheduler 3.11.2
- **Server**: Uvicorn 0.42.0
- **Deployment**: Render.com
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
marketplace/
├── api/
│   ├── routers/
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── offer.py
│   │   ├── order.py
│   │   └── price_log.py
│   ├── test_inserts/
│   │   └── insert_users.py
│   ├── database.py
│   ├── models.py
│   ├── main.py
│   └── cron_deactivate_offers.py
│
├── database/
│   ├── 1_Create_Users.sql
│   ├── 2_Create_Categories.sql
│   ├── 3_Create_Offers.sql
│   ├── 4_Create_Orders.sql
│   ├── 5_Create_Order_Details.sql
│   ├── 6_Create_Price_Logs.sql
│   ├── 7_Create_Favourites.sql
│   ├── triggers/
│   │   ├── 11_Trigger_Order_Details.sql
│   │   ├── 12_Trigger_Price_Logs.sql
│   │   ├── 13_Trigger_Offers_Quantity.sql
│   │   └── 14_Trigger_Favourites.sql
│   └── test_inserts/
│       ├── 92_Insert_Categories.sql
│       ├── 93_Insert_Offers.sql
│       ├── 94_Insert_Orders.sql
│       ├── 95_Insert_Favourities.sql
│       └── 96_Insert_Order_Details.sql
│
├── .env.example
├── .gitignore
├── Readme.md
├── render.yaml
└── requirements.txt
```


## 📡 API Endpoints

### Users (`/user`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/user/users` | Get all users |
| GET | `/user/users-offers?user_id={id}` | Get user's offers |
| GET | `/user/favorite_offers?user_id={id}` | Get user's favorite offers |
| POST | `/user/Create_user` | Register new user |
| GET | `/user/log_in` | User login |

**Password Security**

- Passwords hashed using bcrypt with salt
- Maximum password length: 72 characters
- Secure login validation

### Categories (`/category`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/category/category` | Get all categories |
| GET | `/category/Subcategory` | Get all subcategories |

### Offers (`/offer`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/offer/all_offers` | Get all offers |
| GET | `/offer/search_offer_by_id?offer_id={id}` | Search offer by ID |
| GET | `/offer/search_active_offers` | Search active offers with filters |
| POST | `/offer/add_offer` | Create new offer |
| PUT | `/offer/change_offer` | Update existing offer |
| PUT | `/offer/extend_offer` | Extend offer duration |

### Orders (`/order`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/order/orders` | Get all orders |
| GET | `/order/order_details` | Get all order details |
| GET | `/order/order_and_order_details?order_id={id}` | Get order with details |
| POST | `/order/take_an_order` | Create new order |
| GET | `/order/get_users_orders_by_id?user_id={id}` | Get user's orders |

### Price Logs (`/price_log`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/price_log/search_price_logs?offer_id={id}` | Get price history |

