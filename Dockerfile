# Base image with Jupyter
FROM jupyter/base-notebook:latest

# Copy your files (no need to copy the current directory again)
COPY requirements.txt .
COPY akvmodel.py .
COPY example.ipynb .
RUN pip install -r requirements.txt  # Install dependencies (optional)

# Expose Jupyter port
EXPOSE 8888

# Start Jupyter Notebook
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--ServerApp.token=test"]