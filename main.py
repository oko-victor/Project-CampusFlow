"""Interactive CampusFlow menu."""
from campusflow.tickets import create_ticket,find_ticket
from campusflow.workflow import assign_ticket,change_status
from campusflow.reports import work_queue,report
from campusflow.storage import load_tickets,save_tickets
DATA_PATH="data/tickets.json"
def display(ticket):
    print(f'{ticket["id"]}: {ticket["title"]} [{ticket["priority"]}] {ticket["status"]} - {ticket["assigned_to"] or "Unassigned"}')
def main():
    try: tickets=load_tickets(DATA_PATH)
    except ValueError as error:
        print(f"Cannot start safely: {error}. Existing data was NOT overwritten.")
        return
    while True:
        print("\n1 Create | 2 List | 3 View | 4 Assign | 5 Status | 6 Queue | 7 Reports | 8 Exit")
        choice=input("Choose: ").strip()
        try:
            if choice=="1":
                title=input("Title: ");kind=input("Category: ");level=input("Urgency: ")
                raw=input("Affected users: ").strip()
                if not raw.isdecimal(): raise ValueError("Affected users must be positive whole numbers")
                display(create_ticket(tickets,title,kind,level,int(raw)))
                save_tickets(DATA_PATH,tickets)
            elif choice=="2":
                for t in tickets: display(t)
            elif choice=="3": display(find_ticket(tickets,input("Ticket ID: ").strip().upper()))
            elif choice=="4":
                display(assign_ticket(tickets,input("Ticket ID: ").strip().upper(),input("Staff name: ")))
                save_tickets(DATA_PATH,tickets)
            elif choice=="5":
                display(change_status(tickets,input("Ticket ID: ").strip().upper(),input("New status: ")))
                save_tickets(DATA_PATH,tickets)
            elif choice=="6":
                for t in work_queue(tickets): display(t)
            elif choice=="7":
                summary=report(tickets)
                print("Total:",summary["total"],"By status:",summary["by_status"],"By priority:",summary["by_priority"])
            elif choice=="8":
                save_tickets(DATA_PATH,tickets);print("Goodbye");return
            else: print("Choose 1 through 8")
        except ValueError as error: print("Error:",error)
if __name__=="__main__": main()
