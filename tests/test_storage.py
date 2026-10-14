import json
import tempfile
import unittest
from pathlib import Path
from campusflow.tickets import create_ticket
from campusflow.storage import save_tickets,load_tickets
class StorageTests(unittest.TestCase):
    def test_roundtrip_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"tickets.json";tickets=[]
            create_ticket(tickets,"Router","Network","high",10)
            save_tickets(path,tickets)
            loaded=load_tickets(path)
            self.assertEqual(loaded[0]["id"],"T001")
            self.assertEqual(create_ticket(loaded,"Screen","Hardware","low",1)["id"],"T002")
    def test_corrupt_json_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"tickets.json";path.write_text("{broken",encoding="utf-8")
            with self.assertRaises(ValueError): load_tickets(path)
    def test_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"tickets.json";tickets=[]
            create_ticket(tickets,"Router","Network","high",10)
            path.write_text(json.dumps(tickets+tickets),encoding="utf-8")
            with self.assertRaises(ValueError): load_tickets(path)
    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(load_tickets(Path(tmp)/"missing.json"),[])
