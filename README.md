# Clear My Fridge

Get recipes based on your available ingredients via the Spoonacular API.  

---

## Requirements

1. `make`  
2. `uv` (for package management)  
3. Docker (optional, for containerized deployment)  
4. Python 3.11  

---

## Setup

### 1. Install `uv` (if not already installed)
```bash
# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or macOS with Homebrew
brew install uv
```
### 2. Clone the repository
```bash
git clone https://github.com/<your-repo>.git
cd <your-repo>
```
### 3. Setup environment variables
```bash
cp -i .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Set your api_key for the Spoonacular API in .streamlit/secrets.toml.

## Local Development
### 4. Initialize and sync dependencies
```bash
make uv-init   # only needed first time
make install   # install all dependencies from uv lockfile
```

### 5. Run the Streamlit app
```bash
make run
```

The app will be available at http://localhost:8501.

# Updating Dependencies
## Add a package:
```bash
uv add <package-name>
make install
```

## Remove a package:
```bash
uv remove <package-name>
make install
```

After updating, the `uv.lock` file ensures consistent installs for all users.