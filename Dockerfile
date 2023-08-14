FROM python:3.11.4 AS builder

WORKDIR /app

RUN python3 -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage 2
FROM python:3.11.4 AS runner

WORKDIR /app

COPY --from=builder /app/venv venv
COPY . .

ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FAST_API=app/main.py

EXPOSE 8000

CMD [ "uvicorn", "--host", "0.0.0.0", "main:app" ]