FROM node:20-alpine

# node & npm are pre-installed on Alpine image

# Set working dir
WORKDIR /app/react-app

# Install npm dependencies
COPY react-app/package*.json /app/react-app/
RUN npm install

# Copy source code files
# COPY holbertonschool-portfolio_project/react-app /app/react-app
COPY react-app /app/react-app


# Configure Vite's default dev port
EXPOSE 5173

# Run Vite dev server, binding to all interfaces so Docker can forward it
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]