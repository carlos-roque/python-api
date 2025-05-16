FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app directory 
COPY app/ ./app/

# Create logs directory with appropriate permissions
RUN mkdir -p /app/logs && chmod 777 /app/logs

# Set environment variables
ENV PORT=5000
ENV API_TOKEN=carlos89-api-token
ENV DEBUG=False

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"] 