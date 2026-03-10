# UET Platform Deployment Guide

This guide provides instructions on how to deploy the UET Platform (Next.js Frontend, Rust API Backend, and PostgreSQL Database) to production environments using Docker and Railway.app.

## Option 1: Deploying with Railway (Recommended)

[Railway.app](https://railway.app) is the easiest way to deploy the UET Platform because it natively supports Nixpacks and Dockerfiles, providing automatic builds and out-of-the-box PostgreSQL with pgvector support.

### 1. Database Setup (PostgreSQL)

1. Create a new project in Railway.
2. Add a new service -> **Database** -> **Add PostgreSQL**.
3. **IMPORTANT**: Standard Railway Postgres does not have `pgvector`. To use semantic search, you should instead deploy a custom Docker image for your database:
   - Add a new service -> **Custom Service** -> **Deploy from Docker Image**.
   - Use the image: `pgvector/pgvector:pg16`
   - Add the necessary environment variables (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`).
   - Add a Persistent Volume to the `/var/lib/postgresql/data` path to ensure data is saved.

### 2. Backend Setup (Rust API)

1. Connect your GitHub repository to Railway.
2. Add a new service from your GitHub repo.
3. In the service settings, go to **Build** -> **Builder** -> **Dockerfile**.
4. Set the **Dockerfile Path** to `/Dockerfile.api`.
5. Add the necessary Environment Variables:
   - `DATABASE_URL`: `postgres://[USER]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]`
   - `JWT_SECRET`: A strong random string for user authentication
   - `RUST_LOG`: `info`
   - `FRONTEND_URL`: The URL where your Next.js app will be hosted
6. Deploy the service. Once built, Railway will assign it a public URL (e.g., `https://api.uet.up.railway.app`).

### 3. Frontend Setup (Next.js)

1. Add another service from the same GitHub repo.
2. In the service settings, go to **Build** -> **Builder** -> **Dockerfile**.
3. Set the **Dockerfile Path** to `/Dockerfile.web`.
4. Add the necessary Environment Variables:
   - `NEXT_PUBLIC_API_URL`: The public URL of your API service (e.g., `https://api.uet.up.railway.app`)
5. Deploy the service. Railway will assign it a public domain for your users to access.

---

## Option 2: Deploying with Docker Compose (VPS / EC2)

If you prefer hosting the platform on your own Virtual Private Server (VPS) such as AWS EC2, DigitalOcean, or Hetzner, you can use the provided `docker-compose.yml`.

### Requirements on your Server
- Ubuntu 22.04 or 24.04 recommended
- Docker Engine installed (`curl -fsSL https://get.docker.com | sh`)
- Docker Compose plugin installed
- At least 2GB of RAM (4GB recommended for Rust compilation)

### Steps

1. **Clone the repository on your server:**
   ```bash
   git clone https://github.com/unityequilibrium/UnityEquilibriumTheory.git
   cd UnityEquilibriumTheory
   ```

2. **Set up Environment Variables:**
   ```bash
   cp .env.example .env
   nano .env
   ```
   *Edit the `.env` file to add your `JWT_SECRET` and update `NEXT_PUBLIC_API_URL` to your server's IP or Domain.*

3. **Build and Run:**
   ```bash
   docker-compose up --build -d
   ```
   This will build the Rust API, Next.js Frontend, and pull the pgvector Database in the background.

4. **Reverse Proxy (Optional but Recommended):**
   It is highly recommended to set up Nginx or Caddy as a reverse proxy in front of your Docker containers to handle SSL/HTTPS (via Let's Encrypt).
   - Point your main domain (e.g., `uet.tech`) to `localhost:3000` (Next.js)
   - Point your API subdomain (e.g., `api.uet.tech`) to `localhost:3001` (Rust API)

### Useful Docker Commands

- **View Logs:**
  ```bash
  docker-compose logs -f
  ```
- **Stop Services:**
  ```bash
  docker-compose down
  ```
- **Rebuild after pushing updates:**
  ```bash
  git pull
  docker-compose up --build -d
  ```
