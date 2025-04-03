# Todo App with Django + Vue

## Production Setup

1. Copy environment template:
   ```bash
   cp docker.env.example docker.env
   ```

2. Edit `docker.env` with your real values

3. Start services:
   ```bash
   docker-compose up --build
   ```

4. Apply database migrations:
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

## Access
- **Frontend**: http://localhost:8080  
- **API Docs**: http://localhost:8000/api  