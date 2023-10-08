# Use the official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /Ecommerce

# Copy the project files into the container
COPY . /Ecommerce

# Install project dependencies
RUN pip install -r requirements.txt

# Expose port 8000 for the Django application
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
