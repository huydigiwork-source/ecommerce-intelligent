FROM python:3.10

WORKDIR /app

COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY .. /app

# Tạo data dir
RUN mkdir -p /app/data

# Script start: chạy scraper + uvicorn
RUN echo '#!/bin/bash\nexport KAGGLE_API_TOKEN="$KAGGLE_API_TOKEN"\npython backend/scraper.py && uvicorn app:app --host 0.0.0.0 --port 8000' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]