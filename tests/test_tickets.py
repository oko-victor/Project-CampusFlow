import copy
import unittest
from campusflow.tickets import create_ticket, priority

class TicketTests(unittest.TestCase):
    def test_critical(self): self.assertEqual(priority("high", 12), "critical")
    def test_high(self): self.assertEqual(priority("high", 2), "high")
    def test_medium(self): self.assertEqual(priority("low", 4), "medium")
    def test_low(self): self.assertEqual(priority("low", 1), "low")
    def test_zero_users(self):
        with self.assertRaises(ValueError): create_ticket([], "Wifi", "Network", "high", 0)
    def test_bool_users(self):
        with self.assertRaises(ValueError): create_ticket([], "Wifi", "Network", "high", True)
    def test_blank_title(self):
        with self.assertRaises(ValueError): create_ticket([], " ", "Network", "high", 4)
    def test_ticket_numbers(self):
        tickets=[]
        self.assertEqual(create_ticket(tickets, "First", "Network", "low", 1)["id"], "T001")
        self.assertEqual(create_ticket(tickets, "Next", "Other", "low", 1)["id"], "T002")

    def test_invalid_creation_never_mutates_existing_tickets(self):
        tickets=[]
        create_ticket(tickets, "Working Wi-Fi", "Network", "low", 1)
        before=copy.deepcopy(tickets)
        invalid_inputs=[
            ("", "Network", "low", 2),
            ("Second", "Unknown", "low", 2),
            ("Second", "Network", "urgent", 2),
            ("Second", "Network", "medium", -1),
            ("Second", "Network", "medium", 2.5),
            ("Second", "Network", "medium", True),
        ]
        for values in invalid_inputs:
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    create_ticket(tickets, *values)
                self.assertEqual(tickets, before)

    def test_priority_precedence_at_ten_users(self):
        self.assertEqual(priority("low", 10), "high")
        self.assertEqual(priority("medium", 10), "high")
        self.assertEqual(priority("high", 10), "critical")

    def test_category_urgency_normalization(self):
        tickets=[]
        ticket=create_ticket(tickets, "  Router down  ", " nEtWoRk ", " HIGH ", 1)
        self.assertEqual(ticket["title"], "Router down")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["priority"], "high")
