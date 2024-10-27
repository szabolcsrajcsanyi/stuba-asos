# Define variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

# Default target
all: setup

# Create virtual environment
$(VENV_DIR)/bin/activate: ./backend/requirements.txt
	@echo "Creating virtual environment..."
	@python3 -m venv $(VENV_DIR)
	@$(PIP) install --upgrade pip
	@$(PIP) install -r ./backend/requirements.txt
	@echo "Virtual environment created and packages installed."

# Clean up virtual environment
clean:
	@echo "Removing virtual environment..."
	@rm -rf $(VENV_DIR)
	@echo "Virtual environment removed."

# Setup target to create venv and install packages
setup: $(VENV_DIR)/bin/activate

# Phony targets
.PHONY: all clean setup
