from openpyxl import load_workbook

class player_imformation:
    def __init__(self,id=None):
        self.id = id
        self.player_data = []
        self.data = {
            "rate":0.0,
            "used_champion_rank3":[],
            "rate_champion_rank3":[],
            "avg_game_time":0.0,
            "avg_kda":0.0,
            "cspm":0.0,
            "dpm":0.0,
            "gpm":0.0
        }
        
        self.game_mode = {
            "blind_pick":"一般對戰",
            "ranked_solo/duo":"單人/雙排",
            "ranked_flex":"彈性積分",
            "aram":"隨機單中"
        }
        self.max_value = {
            "blind_pick":[14,10,663,231],
            "ranked_solo/duo":[14,10,663,231],
            "ranked_flex":[14,10,663,231],
            "aram":[14,15,983,452]
        }

    def set_data(self):
        sheet = load_workbook("data.xlsx")["Sheet"]
        for row in sheet.values:
            if row[0]!=self.id:
                continue
            self.player_data.append([])
            for value in row:
                self.player_data[-1].append(value)
                

    def is_not_exist(self):
        if self.player_data == []:
            return True
        return False

    def get_data(self,mode:str):
        win = 0
        lose = 0
        total = 0
        champion = {}
        playing_time_min = 0
        kda = 0
        cs = 0
        damage = 0
        money = 0
        if mode=="logout":
            return True
        for row in self.player_data:
            if self.game_mode[mode] in row:
                total += 1
                if row[6] in champion:
                    champion[row[6]][0] += 1
                else:
                    champion[row[6]] = [1,0,0]
                if row[2] == "勝":
                    win += 1
                    champion[row[6]][1] += 1
                elif row[2] == "敗":
                    lose += 1
                    champion[row[6]][2] += 1
                playing_time_min += float(row[4].split('m')[0])+float(row[4][-3:-1])/60
                kda = row[7].split('/')
                kda = float(kda[0])+float(kda[2])/float(kda[1])
                cs += float(row[-3].split('(')[0])
                damage += float(row[-2])
                money += float(row[-4].split('k')[0][1:])*1000
        if total==0:
            raise(ValueError("You have not playing this mode ever."))
        self.data["rate"] = win/total
        champion = dict(sorted(champion.items(), key=lambda item: item[1],reverse=True))
        self.data["used_champion_rank3"] = [list(champion.keys())[0],list(champion.keys())[1],list(champion.keys())[2]]
        for v in champion.items():
            champion[v[0]][0] = champion[v[0]][1]/champion[v[0]][0]
        champion = dict(sorted(champion.items(), key=lambda item: item[1],reverse=True))
        self.data["rate_champion_rank3"] = [list(champion.keys())[0],list(champion.keys())[1],list(champion.keys())[2]]
        self.data["avg_game_time"] = playing_time_min / total
        self.data["avg_kda"] = (kda/total)/self.max_value[mode][0]
        if self.data["avg_kda"] > 1:
            self.data["avg_kda"] = 1
        self.data["cspm"] = (cs/total/playing_time_min)/self.max_value[mode][1]
        if self.data["cspm"] > 1:
            self.data["cspm"] = 1
        self.data["dpm"] = (damage/total/playing_time_min)/self.max_value[mode][2]
        if self.data["dpm"] > 1:
            self.data["dpm"] = 1
        self.data["gpm"] = (money/total/playing_time_min)/self.max_value[mode][3]
        if self.data["gpm"] > 1:
            self.data["gpm"] = 1
        return self.data