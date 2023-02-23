import unittest
import station
import json

class TestStation(unittest.TestCase):
  def setUp(self):
    with open("assets/data.json", "r") as f:
      self.data = "".join(f.readlines())

  def test_should_load_from_dict(self):
    dt = json.loads(self.data)
    st = station.Station.from_dict(dt["records"][0]["fields"])
    self.assertEqual(st.id, "59000010")
    self.assertEqual(st.cp, "59350")
    self.assertEqual(st.departement, "Nord")
    self.assertEqual(st.region, "Hauts-de-France")
    self.assertEqual(st.adresse, "72 Avenue du Président John F. Kennedy")
    self.assertEqual(st.epci_nom, "Métropole Européenne de Lille")
    self.assertEqual(st.position.latitude, 50.632)
    self.assertEqual(st.position.longitude, 3.07)
    self.assertTrue(st.flag_automate_24)
    self.assertEqual(len(st.pompes), 1)
    self.assertEqual(len(st.services), 5)
    self.assertListEqual(st.services, ["Boutique alimentaire","Restauration à emporter","Station de gonflage","Services réparation / entretien","Vente de gaz domestique (Butane, Propane)"])

  def test_should_load_from_txt(self):
      dt = station.Station.parse_from_text(self.data)
      self.assertEqual(len(dt), 6)

  def test_should_filter_by_service(self):
    dt = station.Station.parse_from_text(self.data)
    self.assertEqual(len(station.Station.filter_by_service(dt, "Station de gonflage")), 3)

  def test_should_sort_by_carburant(self):
      dt = station.Station.parse_from_text(self.data)
      sorted_stations = station.Station.sort_by_carburant(dt, "SP98")
      self.assertEqual(sorted_stations[0].id, "59000016")


class TestStationService(unittest.TestCase):
  def test_should_return_result(self):
    service = station.StationService()
    ret = service.find_station_by_ville("LOMME")
    self.assertEqual(len(ret), 3)


if __name__ == '__main__':
    unittest.main()
