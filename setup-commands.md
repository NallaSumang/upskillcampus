# Module 1: Folder Structure & Setup

Here are the exact terminal commands required to scaffold the project structure from scratch.

## Backend (Spring Boot) Setup

Using `curl` to fetch the project structure from Spring Initializr:

```bash
# Create the root project directory
mkdir upskillcampus
cd upskillcampus

# Scaffold the Spring Boot backend
curl -G https://start.spring.io/starter.zip \
    -d dependencies=web,data-jpa,h2,lombok \
    -d javaVersion=17 \
    -d type=maven-project \
    -d groupId=com.uct \
    -d artifactId=smartfactory \
    -d name=IndustrialAssetManagementSystem \
    -d packageName=com.uct.smartfactory \
    -o backend.zip

# Unzip the backend and clean up
unzip backend.zip -d backend
rm backend.zip
```

## Frontend (React) Setup

Using `npx` to create a standard React application:

```bash
# Inside the upskillcampus directory, scaffold the React frontend
npx create-react-app frontend

# Navigate to the frontend directory
cd frontend

# Install axios and Tailwind CSS (with its dependencies)
npm install axios
npm install -D tailwindcss postcss autoprefixer

# Initialize Tailwind configuration
npx tailwindcss init -p
```
