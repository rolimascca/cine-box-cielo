set -o errexist
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

pip install -r requirements.txt && python manage.py collectstatic --noinput
if [ "$CREATE_SUPERUSER" = "true" ]; then
  python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
email = "$ADMIN_EMAIL"
password = "$ADMIN_PASSWORD"
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
END
fi



