# Dockerfile for React (npm)

# Stage 1: Build the React application
FROM node:18-alpine3.21 as build

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the application code
COPY . .

RUN npm run build

# Expose the default port
EXPOSE 3000

# Start the React application
CMD ["npm", "start"]
