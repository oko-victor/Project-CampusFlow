"""Engineer B regression tests for workflow, queue, and reporting."""
import unittest

from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status
from campusflow.reports import report, work_queue


class EngineerBTests(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        create_ticket(self.tickets, "Router", "Network", "high", 12)

    def test_blank_and_non_string_assignees_do_not_mutate(self):
        for staff in (" ", None, 7):
            with self.subTest(staff=staff):
                with self.assertRaises(ValueError):
                    assign_ticket(self.tickets, "T001", staff)
                self.assertIsNone(self.tickets[0]["assigned_to"])

    def test_assignment_is_trimmed_and_reassignment_allowed(self):
        assign_ticket(self.tickets, "T001", "  Alex  ")
        self.assertEqual(self.tickets[0]["assigned_to"], "Alex")
        assign_ticket(self.tickets, "T001", "Sam")
        self.assertEqual(self.tickets[0]["assigned_to"], "Sam")

    def test_illegal_transitions_do_not_mutate(self):
        for target in ("resolved", "open", "bogus", None, 5):
            with self.subTest(target=target):
                with self.assertRaises(ValueError):
                    change_status(self.tickets, "T001", target)
                self.assertEqual(self.tickets[0]["status"], "open")

    def test_unassigned_ticket_cannot_start(self):
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "in_progress")
        self.assertEqual(self.tickets[0]["status"], "open")

    def test_full_lifecycle_and_resolved_assignment_block(self):
        assign_ticket(self.tickets, "T001", "Alex")
        change_status(self.tickets, "T001", " IN_PROGRESS ")
        change_status(self.tickets, "T001", "resolved")
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "Sam")
        change_status(self.tickets, "T001", "open")
        self.assertEqual(self.tickets[0]["status"], "open")

    def test_queue_excludes_in_progress_and_resolved(self):
        create_ticket(self.tickets, "Mouse", "Hardware", "low", 1)
        create_ticket(self.tickets, "Screen", "Hardware", "medium", 1)
        assign_ticket(self.tickets, "T001", "Alex")
        change_status(self.tickets, "T001", "in_progress")
        assign_ticket(self.tickets, "T003", "Sam")
        change_status(self.tickets, "T003", "in_progress")
        change_status(self.tickets, "T003", "resolved")
        self.assertEqual([t["id"] for t in work_queue(self.tickets)], ["T002"])

    def test_queue_priority_and_numeric_id_tie_break(self):
        create_ticket(self.tickets, "Other critical", "Network", "high", 11)
        create_ticket(self.tickets, "High", "Network", "high", 1)
        create_ticket(self.tickets, "Medium", "Network", "medium", 1)
        create_ticket(self.tickets, "Low", "Other", "low", 1)
        self.tickets.reverse()
        self.assertEqual(
            [t["id"] for t in work_queue(self.tickets)],
            ["T001", "T002", "T003", "T004", "T005"],
        )

    def test_queue_does_not_mutate_source_order(self):
        create_ticket(self.tickets, "Mouse", "Hardware", "low", 1)
        self.tickets.reverse()
        before = [t["id"] for t in self.tickets]
        work_queue(self.tickets)
        self.assertEqual([t["id"] for t in self.tickets], before)

    def test_report_mixed_statuses_and_priorities(self):
        create_ticket(self.tickets, "High", "Network", "high", 1)
        create_ticket(self.tickets, "Medium", "Other", "medium", 1)
        create_ticket(self.tickets, "Low", "Other", "low", 1)
        assign_ticket(self.tickets, "T001", "Alex")
        change_status(self.tickets, "T001", "in_progress")
        assign_ticket(self.tickets, "T002", "Sam")
        change_status(self.tickets, "T002", "in_progress")
        change_status(self.tickets, "T002", "resolved")
        self.assertEqual(report(self.tickets), {
            "total": 4,
            "by_status": {"open": 2, "in_progress": 1, "resolved": 1},
            "by_priority": {"critical": 1, "high": 1, "medium": 1, "low": 1},
        })

    def test_empty_report_has_all_zero_buckets(self):
        self.assertEqual(report([]), {
            "total": 0,
            "by_status": {"open": 0, "in_progress": 0, "resolved": 0},
            "by_priority": {"critical": 0, "high": 0, "medium": 0, "low": 0},
        })


if __name__ == "__main__":
    unittest.main()
