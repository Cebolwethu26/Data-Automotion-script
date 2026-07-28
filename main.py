import sys
from service_manager import MarketplaceManager


def print_header():
    print("=" * 60)
    print("   MZANSI VERIFIED SERVICES CLI — Anti-Scam Local Directory")
    print("=" * 60)


def display_business(biz):
    status = "VERIFIED [SAFE]" if biz.is_verified else "UNVERIFIED [PROCEED WITH CAUTION]"
    print(f"\nID:          {biz.biz_id}")
    print(f"Business:    {biz.name}")
    print(f"Category:    {biz.category}")
    print(f"Location:    {biz.location.title()}")
    print(f"Contact:     {biz.contact}")
    print(f"Trust State: {status}")
    print(f"Rating:      {biz.average_rating} / 5.0 ({len(biz.reviews)} reviews)")
    if biz.reviews:
        print("  Recent Reviews:")
        for r in biz.reviews[-2:]:
            print(f"   - [{r.rating}/5] {r.reviewer_name}: \"{r.comment}\"")
    print("-" * 40)


def main():
    manager = MarketplaceManager()

    while True:
        print_header()
        print("1. Search Local Services (e.g., Nail Tech in Boksburg)")
        print("2. Register a Small Business")
        print("3. Verify a Business (Anti-Scam Check)")
        print("4. Leave a Review for a Service")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ").strip()

        if choice == "1":
            loc = input("\nEnter your location (e.g., Boksburg): ").strip()
            cat = input("Enter category (e.g., Nail Tech, Mechanic) [Press Enter for All]: ").strip()
            ver_only = input("Show verified businesses only to avoid scams? (y/n): ").strip().lower() == 'y'

            results = manager.search_services(location=loc, category=cat if cat else None, verified_only=ver_only)

            print(f"\n--- Found {len(results)} service(s) matching your search ---")
            for biz in results:
                display_business(biz)

        elif choice == "2":
            print("\n--- Register Your Small Business ---")
            name = input("Business Name: ").strip()
            category = input("Category (e.g., Nail Tech, Catering): ").strip()
            location = input("Location/City (e.g., Boksburg): ").strip()
            contact = input("Contact Info (Phone/Email): ").strip()
            reg_num = input("Registration/CIPC Number (Optional, for instant verification): ").strip()

            biz = manager.register_business(name, category, location, contact, reg_num)
            print(f"\n[SUCCESS] Business '{biz.name}' registered successfully with ID: {biz.biz_id}")

        elif choice == "3":
            print("\n--- Verify Business Registration ---")
            biz_id = input("Enter Business ID (e.g., BIZ-103): ").strip()
            reg_num = input("Enter Business Registration / CIPC Number: ").strip()

            biz_match = next((b for b in manager.businesses if b.biz_id.upper() == biz_id.upper()), None)
            if biz_match:
                if biz_match.verify_business(reg_num):
                    manager.save_data()
                    print(f"\n[VERIFIED] {biz_match.name} is now verified and marked safe!")
                else:
                    print("\n[FAILED] Invalid registration number. Verification denied.")
            else:
                print("\n[ERROR] Business ID not found.")

        elif choice == "4":
            print("\n--- Rate & Review a Service ---")
            biz_id = input("Enter Business ID to review: ").strip()
            reviewer = input("Your Name: ").strip()
            try:
                rating = float(input("Rating (1.0 to 5.0): ").strip())
                comment = input("Review Comment: ").strip()

                if manager.add_review_to_business(biz_id, reviewer, rating, comment):
                    print("\n[SUCCESS] Thank you! Your review has been recorded.")
                else:
                    print("\n[ERROR] Business ID not found.")
            except ValueError:
                print("\n[ERROR] Invalid rating input. Please enter a number.")

        elif choice == "5":
            print("\nThank you for using Mzansi Verified Services. Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please pick between 1 and 5.")

        input("\nPress Enter to return to menu...")


if __name__ == "__main__":
    main()
