import unittest
from campusflow.tickets import create_ticket,priority
class TicketTests(unittest.TestCase):
    def test_critical(self): self.assertEqual(priority("high",12),"critical")
    def test_high(self): self.assertEqual(priority("high",2),"high")
    def test_medium(self): self.assertEqual(priority("low",4),"medium")
    def test_low(self): self.assertEqual(priority("low",1),"low")
    def test_zero_users(self):
        with self.assertRaises(ValueError): create_ticket([],"Wifi","Network","high",0)
    def test_bool_users(self):
        with self.assertRaises(ValueError): create_ticket([],"Wifi","Network","high",True)
    def test_blank_title(self):
        with self.assertRaises(ValueError): create_ticket([]," ","Network","high",4)
    def test_ticket_numbers(self):
        tickets=[]
        self.assertEqual(create_ticket(tickets,"First","Network","low",1)["id"],"T001")
        self.assertEqual(create_ticket(tickets,"Next","Other","low",1)["id"],"T002")
