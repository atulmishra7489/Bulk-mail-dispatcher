import csv
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



def check_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError as e:
        return False


try: 
    with open('BULKEMAIL.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            current_email = row["Email Address"]
            if check_email(current_email):
                print(current_email, " : valid")
            else:
                print(current_email, " : Not valid")
except Exception as e:
    print(e)
    print("Something went wrong")
# {'email': 'foo@bar.com', 'status': 'valid'}