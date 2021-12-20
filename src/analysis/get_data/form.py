import openpyxl
import csv

def export_to_xlsx(match_data:list, file_name:str):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(list(match_data[0].keys()))
    for d in match_data:
        sheet.append(list(d.values()))
    wb.save(file_name)

def read_csv_reply(filename:str)->list:
    with open(filename, newline='', encoding="utf-8") as csvfile:
        player_data = []
        rows = csv.reader(csvfile)
        for row in rows:
            player_data.append((row[2], row[3]))
        return player_data[1:]