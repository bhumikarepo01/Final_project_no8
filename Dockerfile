# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port your Flask app runs on
EXPOSE 5000

# Run the Flask app
# CMD ["python", "run.py"]

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
