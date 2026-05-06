import sys

class EconetUSSD:
    def __init__(self):
        # Simulated backend balances for the user
        self.airtime_balance = 5.00
        self.ecocash_balance = 50.00
        
        # State tracking for USSD navigation
        self.is_active = False
        self.current_menu = 'idle'
        self.previous_menus = []

    def start_session(self):
        """Initializes the USSD listener, waiting for a valid shortcode."""
        print("Phone Simulator Active. (Dial *143# for Smart Data, 'q' to quit)")
        while True:
            dial = input("\nDial: ").strip()
            
            if dial.lower() == 'q':
                print("Phone switched off.")
                sys.exit(0)
            elif dial == '*143#':
                self.is_active = True
                self.current_menu = 'main'
                self.previous_menus = []
                self._run_ussd_loop()
            else:
                print("USSD code running...\nConnection problem or invalid MMI code.")

    def _run_ussd_loop(self):
        """Main state machine loop handling the active USSD session."""
        while self.is_active:
            # 1. Render the current menu based on state
            self._render_menu()
            
            # 2. Capture user input
            choice = input("\nReply: ").strip()
            
            # 3. Handle universal navigation controls
            if choice == 'cancel' or choice == '':
                self._terminate("Session cancelled.")
                continue
            elif choice == '0' and self.current_menu != 'main':
                self._navigate_back()
                continue

            # 4. Route input to the specific state handler
            self._route_input(choice)

    def _render_menu(self):
        """Displays the text for the current state."""
        print("\n" + "="*30)
        if self.current_menu == 'main':
            print("Econet Smart Data")
            print("1. Data Bouquets")
            print("2. Voice Bundles")
            print("3. Account Balance")
            print("Cancel")
        
        elif self.current_menu == 'data_bouquets':
            print("Select Bouquet Type:")
            print("1. Daily Bouquets")
            print("2. Weekly Bouquets")
            print("3. Monthly Bouquets")
            print("0. Back")
        
        elif self.current_menu == 'daily_data':
            print("Daily Data:")
            print("1. 50MB @ $0.50")
            print("2. 150MB @ $1.00")
            print("3. 600MB @ $2.00")
            print("0. Back")
        
        elif self.current_menu == 'payment_method':
            print("Select Payment Method:")
            print("1. Airtime")
            print("2. EcoCash")
            print("0. Back")

    def _route_input(self, choice: str):
        """Directs the user choice to the logic appropriate for the current state."""
        if self.current_menu == 'main':
            if choice == '1':
                self._navigate_to('data_bouquets')
            elif choice == '2':
                self._terminate("Voice Bundles under maintenance.")
            elif choice == '3':
                self._terminate(f"Your Airtime Balance is ${self.airtime_balance:.2f}. EcoCash: ${self.ecocash_balance:.2f}")
            else:
                print("Invalid choice.")

        elif self.current_menu == 'data_bouquets':
            if choice == '1':
                self._navigate_to('daily_data')
            elif choice == '2':
                self._terminate("Weekly Bouquets coming soon.")
            elif choice == '3':
                self._terminate("Monthly Bouquets coming soon.")
            else:
                print("Invalid choice.")

        elif self.current_menu == 'daily_data':
            # Map choice to a (Package Name, Price) tuple
            packages = {
                '1': ("50MB Daily", 0.50),
                '2': ("150MB Daily", 1.00),
                '3': ("600MB Daily", 2.00)
            }
            if choice in packages:
                # Store the selected package in the instance for the next state
                self.pending_purchase = packages[choice]
                self._navigate_to('payment_method')
            else:
                print("Invalid choice.")

        elif self.current_menu == 'payment_method':
            package_name, price = self.pending_purchase
            
            if choice == '1': # Airtime
                if self.airtime_balance >= price:
                    self.airtime_balance -= price
                    self._terminate(f"Success. You bought {package_name}. New Airtime Bal: ${self.airtime_balance:.2f}")
                else:
                    self._terminate("Insufficient Airtime balance.")
            
            elif choice == '2': # EcoCash
                if self.ecocash_balance >= price:
                    self.ecocash_balance -= price
                    self._terminate(f"Success. You bought {package_name}. New EcoCash Bal: ${self.ecocash_balance:.2f}")
                else:
                    self._terminate("Insufficient EcoCash balance.")
            else:
                print("Invalid choice.")

    def _navigate_to(self, new_menu: str):
        """Pushes current state to history and updates state."""
        self.previous_menus.append(self.current_menu)
        self.current_menu = new_menu

    def _navigate_back(self):
        """Pops the last state from history."""
        if self.previous_menus:
            self.current_menu = self.previous_menus.pop()
        else:
            self.current_menu = 'main'

    def _terminate(self, message: str):
        """Ends the USSD session and displays a final network message."""
        print("\n" + "="*30)
        print(message)
        print("="*30 + "\n")
        self.is_active = False

if __name__ == "__main__":
    app = EconetUSSD()
    try:
        app.start_session()
    except KeyboardInterrupt:
        print("\nSimulator terminated safely, Boss.")
        sys.exit(0)
