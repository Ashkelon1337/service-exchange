# 🛠 Service Exchange System

A comprehensive service exchange platform that integrates a Telegram bot for end-users with a robust REST API and an admin dashboard for data management. 

👉 **Live Demo:** [Ashkelon Service Bot](https://t.me/Ashkelon_Service_Bot)

---

## 🚀 Tech Stack

* **Backend:** FastAPI (Python 3.11+)
* **Telegram Bot:** aiogram 3.x (driven by Webhooks)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy 2.0 (Async)
* **Admin Interface:** SQLAdmin
* **Deployment / Hosting:** Render

---

## 🏗 Project Architecture

The entire application runs as a **single process on Render**. This architectural choice drastically reduces resource consumption and ensures instant, real-time data synchronization between the Telegram bot and the REST API.

* **API:** Exposes secure endpoints to retrieve and manage services and user profiles.
* **Telegram Bot:** Acts as the primary interface, handling real-time interactions between clients and service providers.
* **Admin Panel:** Features a built-in management interface accessible via designated `ADMIN_IDS` directly in Telegram, alongside a full-scale web interface at `/admin` for comprehensive browser-based database control.

---

## 📁 Directory Structure

* `api/` — FastAPI core logic, route endpoints, and web admin configurations.
* `bot/` — Telegram bot handlers, custom keyboards, and conversation flow logic.
* `database/` — Async SQLAlchemy models, database connections, and migrations.
* `run.py` — The unified application entry point combining FastAPI and aiogram via Webhooks.
* `config.py` — Environment variables management and database connection setups.

[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Ashkelon_Service_Bot)
