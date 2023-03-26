# Todoist #
## Дипломный проект ##
### Cтек (python3.10, Django, Postgres) ###
1. Install requirements:  

    ```pip install -r requirements.txt```
    
2. Create .env file with constants:
    ```python
   SECRET_KEY
    DEBUG
    DATABASE_URL

3. Create migrations:  
```./manage.py makemigrations```
4. Apply migrations:  
```./manage.py migrate```
5. Run server:  
```./manage.py runserver```
