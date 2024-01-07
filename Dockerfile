# Use an official Python runtime as a parent image
FROM python:3.11.2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright and its dependencies
RUN playwright install --with-deps chromium

# Expose the port gunicorn will listen on
EXPOSE 8000

# Finally, run gunicorn.
CMD ["gunicorn", "guitainer.wsgi:application", "--bind", "0.0.0.0:8000"]