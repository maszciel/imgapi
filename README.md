# **Image Upload API**
This Django REST Framework API allows an authenticated user to upload an image.

## **Set Up**
1. Clone this repository and change directory to the project folder.
2. Run docker-compose build
3. Run docker-compose run --rm app sh -c "python manage.py makemigrations && python manage.py migrate && python manage.py createsuperuser"
4. Type email and password.
5. Run docker-compose up
6. Visit 'localhost:8000/admin'

## **Authenticating with Swagger UI**
1. Create a user via admin panel
2. Visit localhost:8000/api/docs
3. Scroll down and expand on /token/
4. Click 'Try it out' and log in
5. Copy the token from the output
6. Scroll up and click Authorize
7. In 'tokenAuth (apiKey)' section type 'Token ' and paste the token

## **Endpoints**
- localhost:8000/admin
- localhost:8000/api/docs
- localhost:8000/image
- localhost:8000/image/create
- localhost:8000/expiring-link
- localhost:8000/expiring-link/create
- localhost:8000/expiring-link/{id}
