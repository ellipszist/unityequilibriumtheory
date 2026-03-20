# UET Platform — Authentication & Account Flow Audit

## 1. Auth Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌───────────────┐
│   Login Page     │────▶│  uet_api (Rust)  │────▶│  PostgreSQL   │
│  /auth/login     │     │  localhost:3001   │     │  (Users, JWT) │
└─────────────────┘     └──────────────────┘     └───────────────┘
         │                        │
         │ access_token           │ JWT verify
         ▼                        ▼
┌─────────────────┐     ┌──────────────────┐
│  Account Page    │────▶│  /api/auth/me    │
│  /account        │     │  /api/auth/quota │
│  (localStorage)  │     │  /api/auth/keys  │
└─────────────────┘     └──────────────────┘
```

## 2. Login Flow

| Step | Action | Code Location |
|------|--------|---------------|
| 1 | User enters email + password | `src/app/[locale]/auth/login/page.tsx` |
| 2 | POST `localhost:3001/api/auth/login` | login page `handleSubmit()` |
| 3 | Backend validates credentials, returns JWT | `uet_api` (Rust Axum) |
| 4 | Store `access_token`, `refresh_token`, `user` in **localStorage** | login page line 35-37 |
| 5 | Redirect to `/account` | login page line 40 |

## 3. Account Page Auth Check

| Step | Action | Code Location |
|------|--------|---------------|
| 1 | `useEffect` checks `localStorage.getItem("access_token")` | account page line 147-157 |
| 2 | **Dev mode**: if no token, auto-set `dev_mock_token` + mock user | account page line 151-153 |
| 3 | `fetchData()` calls 3 APIs with `Authorization: Bearer <token>` | account page line 168-228 |
| 4 | **Dev mode**: if API fails, fall back to mock data silently (2s timeout) | account page line 170-198 |
| 5 | **Prod mode**: if API returns non-ok, clear tokens → redirect to `/auth/login` | account page line 212-217 |

## 4. Logout Flow

| Step | Action | Code Location |
|------|--------|---------------|
| 1 | User clicks logout button | account page `logout()` |
| 2 | Remove `access_token`, `refresh_token`, `user` from localStorage | account page line 275-277 |
| 3 | Redirect to `/` | account page line 278 |

## 5. Registration Flow

| Step | Action | Code Location |
|------|--------|---------------|
| 1 | User enters email + password + display name | `src/app/[locale]/auth/register/page.tsx` |
| 2 | POST `localhost:3001/api/auth/register` | register page `handleSubmit()` |
| 3 | Backend creates user, sends verification email | `uet_api` |
| 4 | Show "Check your email" screen | register page line 49-66 |

## 6. OAuth Flow

| Provider | URL | Code Location |
|----------|-----|---------------|
| Google | `localhost:3001/api/auth/oauth/google` | login page line 135 |
| GitHub | `localhost:3001/api/auth/oauth/github` | login page line 147 |

## 7. Token Storage

| Key | Value | Used By |
|-----|-------|---------|
| `access_token` | JWT string | All API calls (Authorization header) |
| `refresh_token` | JWT string | Token refresh (not yet implemented on frontend) |
| `user` | JSON string (id, email, etc.) | UI display |

## 8. API Endpoints Used by Frontend

| Endpoint | Method | Page | Purpose |
|----------|--------|------|---------|
| `localhost:3001/api/auth/login` | POST | Login | Authenticate |
| `localhost:3001/api/auth/register` | POST | Register | Create account |
| `localhost:3001/api/auth/me` | GET | Account | Get user profile |
| `localhost:3001/api/auth/quota` | GET | Account | Get usage quota |
| `localhost:3001/api/auth/api-keys` | GET/POST/DELETE | Account | Manage API keys |
| `localhost:3001/api/auth/oauth/google` | GET | Login | Google OAuth |
| `localhost:3001/api/auth/oauth/github` | GET | Login | GitHub OAuth |
| `/api/wallet` | GET/POST | Account (Wallet tab) | Wallet data |
| `/api/wallet/transfer` | POST | Account (Wallet tab) | Send UET |
| `/api/compute` | GET | Account (Mining tab) | Mining stats |
| `/api/chat` | POST | Chat/KB page | Knowledge search |

## 9. Current Issues & Recommendations

### Issues Found
1. **Hard-coded API_BASE** — `localhost:3001` is hard-coded in login, register, and account pages. Should use env variable.
2. **No token refresh** — `refresh_token` is stored but never used to refresh expired `access_token`.
3. **No middleware auth guard** — Any page can be accessed without auth; protection is only client-side redirect.
4. **localStorage only** — Tokens in localStorage are vulnerable to XSS. Consider httpOnly cookies for production.

### Recommendations
1. Move `API_BASE` to `NEXT_PUBLIC_API_URL` env variable.
2. Implement token refresh logic or use session-based auth.
3. Add Next.js middleware to protect `/account` routes server-side.
4. For production: migrate to httpOnly cookie-based auth flow.
