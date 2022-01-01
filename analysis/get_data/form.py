import csv

def export_to_csv(match_data:list, file_name:str):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list(match_data[0].keys()))
        for d in match_data:
            writer.writerow(list(d.values()))

def read_csv_reply(filename:str)->list:
    with open(filename, newline='', encoding="utf-8") as csvfile:
        player_data = []
        rows = csv.reader(csvfile)
        for row in rows:
            player_data.append(row[3])
        return player_data