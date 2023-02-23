import json, requests


class Position:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


class Pompe:
    def __init__(self, prix, libelle):
        self.prix = prix
        self.libelle = libelle


class Station:

    def __init__(self, id, cp, ville, departement, region, adresse, epci_nom, latitude, longitude, flag_automate_24, pompes, services):
        self.id = id
        self.cp = cp
        self.ville = ville
        self.departement = departement
        self.region = region
        self.adresse = adresse
        self.epci_nom = epci_nom
        self.position = Position(latitude, longitude)
        self.flag_automate_24 = flag_automate_24
        self.pompes = pompes
        self.services = services

    @staticmethod
    def from_dict(data):
        return Station(data["id"], data["com_code"], data["ville"], data["dep_name"], data["reg_name"], data["adresse"]
        , data["epci_name"], data["geom"][0], data["geom"][1], data["horaires_automate_24_24"] == "Non",
        [Pompe(data["prix_valeur"], data["prix_nom"])], data.get("services_service", "").split("//"))

    def parse_from_text(data: str) -> dict:

        recordedStationsList = json.loads(data)["records"]
        stationsList = list()

        for s_raw in recordedStationsList:
            station = Station.from_dict(s_raw["fields"])
            merged = False

            for s in stationsList:
                if station.id == s.id:
                    stationsList[stationsList.index(s)].pompes.append(s.pompes[0])
                    merged = True

            if not merged:
                stationsList.append(station)

        return stationsList

    @staticmethod
    def sort_by_carburant(stations, carburant):
        stations_carburant = list()
        for s in stations:
            for p in s.pompes:
                if p.libelle == carburant:
                    stations_carburant.append(s)
        return stations_carburant

    @staticmethod
    def filter_by_service(stations, service):

        stations_service = list()
        for s in stations:
            if service in s.services:
                stations_service.append(s)
        return stations_service


class StationService:
    def __init__(self):
        pass

    def find_station_by_ville(self, ville):
        url = "https://data.economie.gouv.fr/api/records/1.0/search/?"
        value = {"dataset": "prix-carburants-fichier-instantane-test-ods-copie", "q": f"ville={ville.upper()}"}
        req = requests.get(url, params=value)
        data = Station.parse_from_text(req.content.decode("utf-8"))
        return data
