import csv

input_file = 'customers.csv'          # путь к исходному CSV
output_file = 'customers_fixed.csv'       # путь к новому CSV

with open(input_file, mode='r', encoding='utf-8') as infile, \
     open(output_file, mode='w', encoding='utf-8', newline='') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)  # ВСЕ значения в кавычки

    for row in reader:
        writer.writerow(row)

print("CSV успешно преобразован!")
