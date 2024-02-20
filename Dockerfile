
FROM python:3.12.2-alpine3.18
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run Django app when the container launches
CMD ["python", "sce_final_project/manage.py", "runserver", "0.0.0.0:8000"]