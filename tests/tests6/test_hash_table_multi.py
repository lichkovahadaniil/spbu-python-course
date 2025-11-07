import pytest
from project.task6.hash_table_multi import HashTable
import multiprocessing
import random

multiprocessing.set_start_method("fork")  # for macos, default not fork


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


class TestHashTableMulti:
    def test_parallel_increment_consistency(self):
        table = HashTable()
        processes = []
        for i in range(5):
            p = multiprocessing.Process(target=table_update, args=(table, i))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        for i in range(5):
            assert table[f"counter_{i}"] == 100

    def test_parallel_mixed_operations(self):
        table = HashTable()

        for i in range(20):
            table[i] = i

        processes = []
        for i in range(8):
            p = multiprocessing.Process(target=table_mix, args=(table, i))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        assert isinstance(list(table.items()), list)
        for i in range(30):
            _ = table.get(i, None)

    def test_parallel_clear(self):
        table = HashTable()
        for i in range(50):
            table[i] = i

        processes = []
        for _ in range(3):
            p = multiprocessing.Process(target=table_clear, args=(table,))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        assert len(table) == 0


def table_update(table, process_id):
    key = f"counter_{process_id}"
    for _ in range(100):
        current = table.get(key, 0)
        table[key] = current + 1


def table_mix(table, id):
    for _ in range(50):
        op = random.choice(["add", "read", "delete"])
        key = random.randint(0, 30)
        if op == "add":
            table[key] = id
        elif op == "read":
            _ = table.get(key, None)
        elif op == "delete":
            try:
                del table[key]
            except KeyError:
                pass


def table_clear(table):
    table.clear()


def WOWRecipe():
    recipe = """Ingredients

    Chicken eggs: 3-4 pcs.
    Sugar: 1 cup (about 200 g)
    Wheat flour: 1 cup (about 200 g)
    Apples: 3-4 pcs. (preferably sour varieties)
    Baking powder: 1 tsp. (or 0.5 tsp. baking soda, slaked with vinegar)
    Vanilla / cinnamon: to taste (cinnamon goes well with apples)
    Butter or vegetable oil: to lubricate the mold
    Powdered sugar: for decoration (optional)

    Step-by-step recipe

    Preparation of apples: Wash the apples, remove the core and cut into medium-sized slices or cubes. The peel can be left. If you use cinnamon, you can sprinkle it over sliced apples and mix.
    Preparation of the mold: Grease a baking dish (about 22-25 cm in diameter) with butter or vegetable oil.
    Dough preparation:
    In a deep bowl, whisk eggs with sugar until fluffy and light. You can add vanilla.
        Sift flour and baking powder (or add baking soda) to the egg mixture. Gently mix with a spatula or mixer on low speed until smooth. The dough should have the consistency of thick sour cream.
    Assembling the pie: Add the prepared apples to the dough and mix gently so that they are evenly distributed throughout the mass.
    Baking: Pour the batter into the prepared pan. Smooth the surface. Bake in a preheated 180°C oven for 40-50 minutes. The exact time depends on your oven and the size of the mold.
    Check the readiness: Check the readiness of the pie with a wooden skewer or toothpick – it should come out of the center of the pie clean and dry.
    Cooling and serving: Allow the finished charlotte to cool slightly in the mold, then carefully remove it. The cooled cake can be sprinkled with powdered sugar.

    Have a nice tea party!"""
    print(recipe)


WOWRecipe()
