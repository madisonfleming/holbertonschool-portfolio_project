FROM ubuntu:22.04

# install dependencies
RUN apt-get update && apt-get install -y --fix-missing \
    python3 \
    python3-pip \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    default-mysql-client

# Set working dir & copy code files
WORKDIR /app
COPY holbertonschool-portfolio_project/requirements.txt .
COPY holbertonschool-portfolio_project/scripts /app/scripts
COPY holbertonschool-portfolio_project/app /app/app

# Install app dependencies
RUN pip install -r requirements.txt

# Set PYTHONPATH else Docker cracks it
ENV PYTHONPATH=/app

# Configure port
EXPOSE 8000

# Run app inside container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]