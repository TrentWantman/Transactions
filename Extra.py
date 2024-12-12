class InMemoryDB:
    def __init__(self):
        # Main database state
        self._data = {}
        # Temporary transaction data
        self._transaction_data = None
        # Flag to track if a transaction is in progress
        self._transaction_in_progress = False

    def get(self, key):
        """
        Retrieve the value for a given key.
        If in a transaction, check transaction data first.
        If not in a transaction, check main data.
        Returns None if key doesn't exist.
        """
        if self._transaction_in_progress and key in self._transaction_data:
            return self._transaction_data[key]
        
        return self._data.get(key)

    def begin_transaction(self):
        """
        Start a new transaction.
        Raises an exception if a transaction is already in progress.
        """
        if self._transaction_in_progress:
            raise Exception("Transaction already in progress")
        
        # Create a copy of current data to track changes
        self._transaction_data = dict(self._data)
        self._transaction_in_progress = True
        print("Transaction started.")

    def put(self, key, value):
        """
        Update or insert a key-value pair.
        Raises an exception if no transaction is in progress.
        """
        if not self._transaction_in_progress:
            raise Exception("No transaction in progress")
        
        # Update the transaction data
        self._transaction_data[key] = value
        print(f"Updated {key} to {value} in transaction.")

    def commit(self):
        """
        Commit the current transaction.
        Raises an exception if no transaction is in progress.
        """
        if not self._transaction_in_progress:
            raise Exception("No transaction in progress")
        
        # Update main data with transaction changes
        self._data = self._transaction_data
        
        # Reset transaction state
        self._transaction_data = None
        self._transaction_in_progress = False
        print("Transaction committed.")

    def rollback(self):
        """
        Roll back the current transaction.
        Raises an exception if no transaction is in progress.
        """
        if not self._transaction_in_progress:
            raise Exception("No transaction in progress")
        
        # Reset transaction state without applying changes
        self._transaction_data = None
        self._transaction_in_progress = False
        print("Transaction rolled back.")

def main():
    db = InMemoryDB()
    
    while True:
        print("\n--- In-Memory Database Menu ---")
        print("1. Get value")
        print("2. Begin transaction")
        print("3. Put value")
        print("4. Commit")
        print("5. Rollback")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        try:
            if choice == '1':
                # Get value
                key = input("Enter key to retrieve: ")
                value = db.get(key)
                print(f"Value for {key}: {value}")
            
            elif choice == '2':
                # Begin transaction
                db.begin_transaction()
            
            elif choice == '3':
                # Put value
                key = input("Enter key: ")
                value = int(input("Enter value: "))
                db.put(key, value)
            
            elif choice == '4':
                # Commit
                db.commit()
            
            elif choice == '5':
                # Rollback
                db.rollback()
            
            elif choice == '6':
                # Exit
                print("Exiting database...")
                break
            
            else:
                print("Invalid choice. Please try again.")
        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
