class HashTable:
    def __init__(self, capacity=40):
        self.capacity = capacity
        self.table = [None] * capacity

    # Space-Time Complexity: O(1)
    def _hash(self, key):
        """Hash function to convert key to an index"""
        return hash(key) % self.capacity

    # Space-Time Complexity: O(n)
    def insert(self, key, value):
        """Insert or update a key-value pair in the hash table"""
        index = self._hash(key)

        if self.table[index] is None:
            self.table[index] = [(key, value)]
        else:
            found = False
            # Iterate through existing list of key-value pairs in current bucket
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    # Update value if key is found
                    self.table[index][i] = (key, value)
                    found = True
                    break
            if not found:
                self.table[index].append((key, value))

    # Space-Time Complexity: O(n)
    def lookup(self, key):
        """Retrieve a value by key"""
        index = self._hash(key)

        if self.table[index] is not None:
            # Search for key in this bucket
            for k, v in self.table[index]:
                if k == key:
                    return v
        return None

    # Space-Time Complexity: O(n)
    def delete(self, key):
        """Remove a key-value pair from the hash table"""
        index = self._hash(key)

        if self.table[index] is not None:
            # Iterate through existing list of key-value pairs in current bucket
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    # Remove key-value pair
                    del self.table[index][i]
                # If bucket is now empty, set it to None
                if not self.table[index]:
                    self.table[index] = None

    def __str__(self):
        return str(self.__dict__)
