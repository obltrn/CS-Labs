import sys


class LRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}

    # Gets the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
    def get(self, key):
        if key in self.cache:
            return self.cache[key]

        return -1

    # Insert or replace the value if the given key is not already in the cache. When
    # the cache reaches its maximum capacity, it should invalidate the least recently used item
    # before inserting a new item.
    def put(self, key, value):
        if key in self.cache:  # if key is in cache we update the value
            self.cache[key] = value

        else:  # otherwise we add the new value and remove the oldest if needed
            if self.size() == self.max_capacity():
                self.remove()
            self.cache.update({key: value})

    # Returns the number of key/value pairs currently stored in the cache
    def size(self):
        return len(self.cache)

    # Returns the maximum capacity of the cache
    def max_capacity(self):
        return self.capacity

    def remove(self):
        min_value = sys.maxint
        old_key = -1
        for key, value in self.cache.iteritems():
            if value < min_value:
                min_value = value
                old_key = key

        self.cache.pop(old_key)

    def print_cache(self):
        print(self.cache)


def problem_b(word_list):
    dictionary = {}
    for word in word_list:
        if word not in dictionary:
            dictionary[word] = 0
        else:
            dictionary[word] += 1

    count = 0
    for key in sorted(dictionary.keys(), key=lambda item: item[1]):

        print ("Key: %s\tValue: %s" % (key, dictionary[key]))


def main():
    capacity = 4
    ll = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    lru = LRU(capacity)
    value = 0
    for key in ll:
        lru.put(key, value)
        value += 1

    lru.print_cache()

    word_list = ['test', 'test', 'two', 'three', 'fiev', 'wired']
    problem_b(word_list)

main()
