FROM --platform=linux/amd64 python:3.7

# Create the application directory
RUN mkdir /auth
RUN mkdir /saml

# Select as working directory
WORKDIR /auth

# Expose the port app will listen on
EXPOSE 8000

# Copy the requirements file in order to install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

# Copy the rest of the codebase into the image
COPY . /auth

# Start Gunicorn web server
CMD ["gunicorn", "--chdir", "/auth", "app:app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:8000"]