import json

class Waktu():
    def __init__(self, json):
        self.json = json
        self.hari = json['hari']
        self.tanggal = json['tanggal']
        self.bulan = json['bulan']
        self.tahun = json['tahun']
        self.jam = json['jam']
        self.full_time = json['full']
    def __str__(self) -> str:
        return str(json.dumps(self.json, indent=3))