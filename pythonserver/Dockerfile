# python-app/Dockerfile
FROM python:3.8

# Add your application files
COPY . /app

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip3 install -r requirement.txt

# Expose the port your application runs on
EXPOSE 3000



# Command to run your application
CMD ["python3", "pythonserver.py"]