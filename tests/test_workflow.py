import unittest
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket,change_status
from campusflow.reports import work_queue,report
class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tickets=[]
        create_ticket(self.tickets,"Router","Network","high",12)
    def test_unassigned_blocked(self):
        with self.assertRaises(ValueError): change_status(self.tickets,"T001","in_progress")
        self.assertEqual(self.tickets[0]["status"],"open")
    def test_lifecycle(self):
        assign_ticket(self.tickets,"T001","Staff A")
        change_status(self.tickets,"T001","in_progress")
        change_status(self.tickets,"T001","resolved")
        self.assertEqual(self.tickets[0]["status"],"resolved")
        change_status(self.tickets,"T001","open")
        self.assertEqual(self.tickets[0]["status"],"open")
    def test_resolved_assignment_blocked(self):
        assign_ticket(self.tickets,"T001","Staff A")
        change_status(self.tickets,"T001","in_progress")
        change_status(self.tickets,"T001","resolved")
        with self.assertRaises(ValueError): assign_ticket(self.tickets,"T001","Staff B")
    def test_queue_only_open(self):
        create_ticket(self.tickets,"Mouse","Hardware","low",1)
        assign_ticket(self.tickets,"T001","Staff A")
        change_status(self.tickets,"T001","in_progress")
        self.assertEqual([t["id"] for t in work_queue(self.tickets)],["T002"])
    def test_reports_empty(self): self.assertEqual(report([])["total"],0)
    def test_queue_priority_order(self):
        create_ticket(self.tickets,"Software","Software","medium",1)
        create_ticket(self.tickets,"Cable","Hardware","high",2)
        self.assertEqual([t["id"] for t in work_queue(self.tickets)],["T001","T003","T002"])
