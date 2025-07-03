set -o errexist
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

if [ "$CREATE_SUPERUSER" = "true" ]; then
  python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
username = "$ADMIN_USERNAME"
email = "$ADMIN_EMAIL"
password = "$ADMIN_PASSWORD"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
END
fi

