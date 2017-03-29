set path=%path%;C:\Program Files (x86)\Opera\;"C:\Program Files (x86)\Google\Chrome\Application\"

python manage.py dbbackup
@start /b cmd /c chrome http://localhost:8080/
python manage.py runserver 8080

