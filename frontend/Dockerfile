# Node.js base image
FROM node:20-alpine

# Set work directory
WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy package files
COPY package.json pnpm-lock.yaml* ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy project files
COPY . .

# Expose port
EXPOSE 3000

# Development command
CMD ["pnpm", "dev", "--host"]

