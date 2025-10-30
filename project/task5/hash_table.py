from typing import Any, Iterator


class HashTable:
    """a class for the hash table realization"""

    def __init__(self, sz: int = 100) -> None:
        """a constructor for hash table
        args:
            sz (int): the size of the hash table
        """
        self.size = sz
        self.cells: list[list[tuple[Any, Any]]] = [[] for _ in range(self.size)]

    def hashing(self, item: Any) -> int:
        """a func for hashing elements using the remainder of the division
        args:
            item (Any): item for hash
        returns:
            remainder (int) of the division hash(item) on the size (hash is buit-in func)"""
        return hash(item) % self.size

    def __getitem__(self, key: Any) -> Any:
        """getter
        args:
            key (Any): key for get value
        returns:
            item (Any): item from the hash table by 'key'
        raises:
            KeyError: if key isn't found
        """
        ind = self.hashing(key)
        for key_in, val_in in self.cells[ind]:
            if key_in == key:
                return val_in
        raise KeyError

    def __setitem__(self, key: Any, value: Any) -> None:
        """setter
        args:
            key (Any): key for set value
            value (Any): value for set
        """
        ind = self.hashing(key)
        for i in range(len(self.cells[ind])):
            if self.cells[ind][i][0] == key:
                self.cells[ind][i] = (key, value)
                return
        self.cells[ind].append((key, value))

    def __delitem__(self, key: Any) -> None:
        """delete item using the key
        args:
            key (Any): key for acces the item
        raises:
            KeyError: if key isn't found
        """
        ind = self.hashing(key)
        for i in range(len(self.cells[ind])):
            if self.cells[ind][i][0] == key:
                del self.cells[ind][i]
                return
        raise KeyError

    def __contains__(self, key: Any) -> bool:
        """check item availability using the key
        args:
            key (Any): key for acces the item
        returns:
            True if this key in the hash table, else False
        """
        ind = self.hashing(key)
        for i in range(len(self.cells[ind])):
            if self.cells[ind][i][0] == key:
                return True
        return False

    def __len__(self) -> int:
        """overloading the len of the hash table
        returns:
           the len of the hash table (int)
        """
        cnt: int = 0
        for i in range(self.size):
            cnt += len(self.cells[i])
        return cnt

    def __iter__(self) -> Iterator[Any]:
        """overloading the iterator,
        the object can be iterated over and it will return the last current keys until it reaches the end
        returns:
            Iterator[Any], which can give next item in the hash table
        """
        for item in self.cells:
            for key, val in item:
                yield key

    def keys(self) -> Iterator[Any]:
        """method for keys access
        returns:
            Iterator[Any]: allows key iteration
        """
        return iter(self)

    def values(self) -> Iterator[Any]:
        """method for values access
        returns:
            Iterator[Any]: iterator by values
        """
        for cell in self.cells:
            for key, val in cell:
                yield val

    def items(self) -> Iterator[tuple[Any, Any]]:
        """method for keys and values access
        returns:
            Iterator[tuple[Any, Any]]: iterator by keys and values
        """
        for cell in self.cells:
            for key, val in cell:
                yield (key, val)

    def get(self, key: Any, default: Any = None) -> Any:
        """safe method for access to items in the hash table
        args:
            key (Any): key to get item
            default (Any): default value if key not found
        returns:
            Any: default if key not found else Any
        """
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key: Any) -> Any:
        """pop func for hash table
        args:
            key (Any): key, which is pointing to item for remove and return
        returns:
            Any: value associated with the key
        raises:
            KeyError: if key isn't found
        """
        if key in self:
            value = self[key]
            del self[key]
            return value
        else:
            raise KeyError(key)

    def clear(self) -> None:
        """remove all of the pairs (key eith value) from the hash table"""
        for i in range(self.size):
            self.cells[i] = []

    def __repr__(self) -> str:
        """the method for output
        returns:
            str: output value - a table string view"""
        all_cell = []
        for key in self:
            all_cell.append(f"{key}: {self[key]}, ")
        return "{" + "".join(all_cell)[:-2] + "}"
