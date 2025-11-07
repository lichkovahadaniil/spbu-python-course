import pytest
from project.task5.hash_table import HashTable


class TestHashTable:
    def test_create_and_empty_state(self):
        h = HashTable()
        assert len(h) == 0
        assert list(h.items()) == []
        assert repr(h) == "{}"

    def test_set_get_and_in_operator(self):
        h = HashTable()
        h["a"] = 1
        h["b"] = 2
        assert h["a"] == 1
        assert h["b"] == 2
        assert "a" in h
        assert "b" in h
        assert "z" not in h
        assert len(h) == 2

    def test_overwrite_and_delete(self):
        h = HashTable()
        h["x"] = 10
        h["x"] = 99
        assert h["x"] == 99
        del h["x"]
        assert "x" not in h
        with pytest.raises(KeyError):
            _ = h["x"]

    def test_get_and_pop(self):
        h = HashTable()
        h["a"] = 42
        assert h.get("a") == 42
        assert h.get("b", "default") == "default"
        val = h.pop("a")
        assert val == 42
        assert "a" not in h
        with pytest.raises(KeyError):
            h.pop("a")

    def test_clear_and_len(self):
        h = HashTable()
        for i in range(5):
            h[i] = i * 10
        assert len(h) == 5
        h.clear()
        assert len(h) == 0
        assert list(h.keys()) == []
        assert list(h.values()) == []

    def test_iteration_and_items(self):
        h = HashTable()
        pairs = {"x": 1, "y": 2, "z": 3}
        for k, v in pairs.items():
            h[k] = v
        assert set(h.keys()) == set(pairs.keys())
        assert set(h.values()) == set(pairs.values())
        assert set(h.items()) == set(pairs.items())
        assert set(iter(h)) == set(pairs.keys())

    def test_repr_format(self):
        h = HashTable()
        h["alpha"], h["beta"] = 1, 2
        text = repr(h)
        assert text.startswith("{") and text.endswith("}")
        assert "alpha:" in text and "beta:" in text and "1" in text and "2" in text

    def test_collision_resolution(self, monkeypatch):
        h = HashTable(sz=2)

        def fake_hash(x):
            return 0

        monkeypatch.setattr(h, "hashing", fake_hash)

        h["k1"] = 100
        h["k2"] = 200
        h["k3"] = 300

        assert h["k1"] == 100
        assert h["k2"] == 200
        assert h["k3"] == 300
        assert len(h) == 3
        del h["k2"]
        assert "k2" not in h
        assert h["k1"] == 100
        assert h["k3"] == 300
