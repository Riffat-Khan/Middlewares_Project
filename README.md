# Middlewares_Project

This project logs IP addresses and enforces rate-limiting rules based on user roles. It includes middleware for IP logging and rate-limiting, views for user authentication and request logs, and forms for user creation.

## Middleware Functionality

### LogIpMiddleware

The `LogIpMiddleware` is located at `IP_log/middlewares/ip_log.py`. This middleware handles IP logging and rate-limiting.

#### Features

1. **IP Logging**: Logs the IP address of authenticated users when they access the `/ip_logging/` endpoint.
2. **Rate Limiting**:
   - **GOLD**: Maximum of 10 requests per minute.
   - **SILVER**: Maximum of 5 requests per minute.
   - **BRONZE**: Maximum of 2 requests per minute.

If the request limit is exceeded, the middleware returns a `429 Too Many Requests` response.


## URLs

The URL configurations are in `urls.py`:

- **Signup**: `/signup/`
- **Login**: `/login/`
- **Logout**: `/logout/`
- **IP Logging**: `/ip_logging/`

