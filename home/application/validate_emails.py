import csv
with open('csv_file') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         print(row)
# {'email': 'foo@bar.com', 'status': 'valid'}