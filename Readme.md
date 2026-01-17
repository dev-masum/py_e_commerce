# Create Admin user
```curl
curl -X POST http://127.0.0.1:5000/auth/admin/register -H "Content-Type: application/json" -H "X-API-KEY: api-key" -d "{\"name\":\"Super Admin\",\"email\":\"test@gmail.com\",\"password\":\"test\"}"
```