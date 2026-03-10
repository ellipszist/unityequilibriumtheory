# Multi-stage Dockerfile for UET Platform
# Builds: uet_api (Rust backend), uet_web (Next.js frontend)

# ==================== Rust Backend Build ====================
FROM rust:slim-bookworm AS rust-builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y pkg-config libssl-dev protobuf-compiler && rm -rf /var/lib/apt/lists/*

# Copy Cargo workspace files
COPY Cargo.toml Cargo.lock ./
COPY uet_core ./uet_core
COPY uet_kb ./uet_kb
COPY uet_api ./uet_api

# Build the API binary
RUN cargo build --release -p uet_api

# ==================== Node Frontend Build ====================
FROM node:20-alpine AS node-builder

WORKDIR /app

# Copy package files
COPY uet_web/package*.json ./

# Install dependencies
RUN npm ci

# Copy source
COPY uet_web ./

# Build Next.js
RUN npm run build

# ==================== Runtime Stage ====================
FROM debian:bookworm-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy Rust API binary
COPY --from=rust-builder /app/target/release/uet_api /usr/local/bin/uet_api

# Copy Node.js app
COPY --from=node-builder /app/.next ./uet_web/.next
COPY --from=node-builder /app/public ./uet_web/public
COPY --from=node-builder /app/package*.json ./uet_web/
COPY --from=node-builder /app/node_modules ./uet_web/node_modules

# Copy migrations
COPY uet_api/migrations ./migrations

# Environment
ENV RUST_LOG=info
ENV NODE_ENV=production

# Expose ports (API: 3001, Web: 3000)
EXPOSE 3000 3001

# Start script will run both services
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
