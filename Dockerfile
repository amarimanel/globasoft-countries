FROM python:3.10-slim

#On empêche Python d'écrire des fichiers .pyc inutiles
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# un dossier de travail dans le conteneur
WORKDIR /app

# copie la listeet on installe tout
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copie toutle code dans le conteneur
COPY . /app/

# le port 8000 sera utilisé
EXPOSE 8000

#  pour lancer le site quand la boîte s'allume
# Note: On utilise 0.0.0.0 pour que ce soit accessible depuis l'extérieur du conteneur
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]