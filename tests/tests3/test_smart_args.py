import pytest
import copy
from project.task3.smart_args import smart_args, Evaluated, Isolated


class TestEvaluated:
    """tests for Evaluated class"""

    def test_evaluated_creation(self):
        """test creation of Evaluated object"""

        def get_value():
            return 42

        evaluated = Evaluated(get_value)
        assert evaluated.func == get_value

    def test_evaluated_function_call(self):
        """test function call in Evaluated"""

        def get_random():
            return 123

        evaluated = Evaluated(get_random)
        result = evaluated.func()
        assert result == 123

    def test_evaluated_with_lambda(self):
        """test Evaluated with a lambda function"""
        evaluated = Evaluated(lambda: "test")
        result = evaluated.func()
        assert result == "test"

    def test_evaluated_error_on_nested_evaluated(self):
        """test error on creation of Evaluated with another Evaluated"""

        def dummy_func():
            return 1

        evaluated1 = Evaluated(dummy_func)

        with pytest.raises(KeyError, match="no need to combine Isolated and Evaluated"):
            Evaluated(evaluated1)


class TestIsolated:
    """tests for Isolated class"""

    def test_isolated_creation(self):
        """test creation of Isolated object"""
        isolated = Isolated()
        assert isinstance(isolated, Isolated)

    def test_isolated_creation_with_obj(self):
        """test creation of Isolated with an object"""
        obj = [1, 2, 3]
        isolated = Isolated(obj)
        assert isinstance(isolated, Isolated)

    def test_isolated_error_on_evaluated(self):
        """test error on creation of Isolated with Evaluated"""

        def dummy_func():
            return 1

        evaluated = Evaluated(dummy_func)

        with pytest.raises(KeyError, match="no need to combine Isolated and Evaluated"):
            Isolated(evaluated)


class TestSmartArgs:
    """tests for smart_args"""

    def test_smart_args_only_kwargs_requirement(self):
        """test requirement for only keyword-only arguments"""

        @smart_args
        def valid_function(*, x=1):
            return x

        assert valid_function() == 1

        @smart_args
        def invalid_function(x=1):
            return x

        with pytest.raises(AssertionError, match="must be only kwargs"):
            invalid_function(5)

    def test_smart_args_basic_functionality(self):
        """test basic functionality of smart_args"""

        @smart_args
        def simple_function(*, x=1, y=2):
            return x + y

        assert simple_function() == 3

    def test_smart_args_with_isolated(self):
        """test smart_args with Isolated"""

        @smart_args
        def modify_dict(*, d=Isolated()):
            d["modified"] = True
            return d

        original_dict = {"original": True}
        result = modify_dict(d=original_dict)

        assert result["modified"] is True
        assert result["original"] is True

        assert "modified" not in original_dict
        assert original_dict["original"] is True

    def test_smart_args_isolated_with_list(self):
        """test Isolated with a mutable list"""

        @smart_args
        def modify_list(*, lst=Isolated()):
            lst.append("modified")
            return lst

        original_list = [1, 2, 3]
        result = modify_list(lst=original_list)

        assert result == [1, 2, 3, "modified"]

        assert original_list == [1, 2, 3]

    def test_smart_args_isolated_with_nested_structure(self):
        """test Isolated with a nested structure"""

        @smart_args
        def modify_nested(*, data=Isolated()):
            data["nested"]["value"] = "changed"
            return data

        original_data = {"nested": {"value": "original"}, "other": [1, 2, 3]}
        result = modify_nested(data=original_data)

        assert result["nested"]["value"] == "changed"
        assert result["other"] == [1, 2, 3]

        assert original_data["nested"]["value"] == "original"

    def test_smart_args_with_evaluated(self):
        """test smart_args with Evaluated"""
        call_count = 0

        def get_counter():
            nonlocal call_count
            call_count += 1
            return call_count

        @smart_args
        def use_evaluated(*, x=Evaluated(get_counter)):
            return x

        result1 = use_evaluated()
        result2 = use_evaluated()
        result3 = use_evaluated()

        assert result1 == 1
        assert result2 == 2
        assert result3 == 3
        assert call_count == 3

    def test_smart_args_evaluated_with_explicit_arg(self):
        """test Evaluated with an explicitly passed argument"""
        call_count = 0

        def get_counter():
            nonlocal call_count
            call_count += 1
            return call_count

        @smart_args
        def use_evaluated(*, x=Evaluated(get_counter)):
            return x

        result = use_evaluated(x=999)
        assert result == 999
        assert call_count == 0

    def test_smart_args_mixed_defaults(self):
        """test smart_args with mixed default values"""
        call_count = 0

        def get_counter():
            nonlocal call_count
            call_count += 1
            return call_count

        @smart_args
        def mixed_function(
            *, normal=10, evaluated=Evaluated(get_counter), isolated=Isolated()
        ):
            return {"normal": normal, "evaluated": evaluated, "isolated": isolated}

        result1 = mixed_function()
        assert result1["normal"] == 10
        assert result1["evaluated"] == 1
        assert call_count == 1

        result2 = mixed_function()
        assert result2["normal"] == 10
        assert result2["evaluated"] == 2
        assert call_count == 2

    def test_smart_args_evaluated_with_random(self):
        """test Evaluated with a function that returns random values"""
        import random

        def get_random():
            return random.randint(0, 100)

        @smart_args
        def random_function(*, x=get_random(), y=Evaluated(get_random)):
            return x, y

        result1 = random_function()
        result2 = random_function()

        x1, y1 = result1
        x2, y2 = result2

        assert x1 == x2
        assert y1 != y2

    def test_smart_args_isolated_with_class_instance(self):
        """test Isolated with a class instance"""

        class TestClass:
            def __init__(self):
                self.value = 0

            def increment(self):
                self.value += 1

        @smart_args
        def modify_instance(*, obj=Isolated()):
            obj.increment()
            return obj

        original = TestClass()
        result = modify_instance(obj=original)

        assert result.value == 1

        assert original.value == 0

    def test_smart_args_with_tuple_isolation(self):
        """test Isolated with tuples"""

        @smart_args
        def modify_tuple(*, t=Isolated()):
            return t

        original_tuple = (1, 2, 3)
        result = modify_tuple(t=original_tuple)

        assert result == original_tuple
        assert result is original_tuple

    def test_smart_args_with_string_isolation(self):
        """test Isolated with strings"""

        @smart_args
        def modify_string(*, s=Isolated()):
            return s + " modified"

        original_string = "hello"
        result = modify_string(s=original_string)

        assert result == "hello modified"

        assert original_string == "hello"

    def test_smart_args_evaluated_with_side_effects(self):
        """test Evaluated with side effects"""
        counter = 0

        def increment_counter():
            nonlocal counter
            counter += 1
            return counter

        @smart_args
        def use_counter(*, x=Evaluated(increment_counter)):
            return x

        result1 = use_counter()
        result2 = use_counter()
        result3 = use_counter()

        assert result1 == 1
        assert result2 == 2
        assert result3 == 3
        assert counter == 3

    def test_smart_args_isolated_with_custom_class(self):
        """test Isolated with a custom class"""

        class CustomClass:
            def __init__(self, value):
                self.value = value
                self.items = []

            def add_item(self, item):
                self.items.append(item)

        @smart_args
        def modify_custom(*, obj=Isolated()):
            obj.add_item("test")
            obj.value = 999
            return obj

        original = CustomClass(42)
        result = modify_custom(obj=original)

        assert result.value == 999
        assert result.items == ["test"]

        assert original.value == 42
        assert original.items == []

    def test_smart_args_multiple_evaluated(self):
        """test smart_args with multiple Evaluated"""
        call_count1 = 0
        call_count2 = 0

        def get_counter1():
            nonlocal call_count1
            call_count1 += 1
            return f"counter1_{call_count1}"

        def get_counter2():
            nonlocal call_count2
            call_count2 += 1
            return f"counter2_{call_count2}"

        @smart_args
        def multiple_evaluated(*, x=Evaluated(get_counter1), y=Evaluated(get_counter2)):
            return f"{x}_{y}"

        result1 = multiple_evaluated()
        result2 = multiple_evaluated()

        assert result1 == "counter1_1_counter2_1"
        assert result2 == "counter1_2_counter2_2"
        assert call_count1 == 2
        assert call_count2 == 2

    def test_smart_args_isolated_with_nested_mutable(self):
        """test Isolated with deeply nested mutable objects"""

        @smart_args
        def deep_modify(*, data=Isolated()):
            data["level1"]["level2"]["level3"].append("modified")
            return data

        original = {"level1": {"level2": {"level3": ["original"]}}}

        result = deep_modify(data=original)

        assert result["level1"]["level2"]["level3"] == ["original", "modified"]

        assert original["level1"]["level2"]["level3"] == ["original"]

    def test_smart_args_evaluated_with_exception(self):
        """test Evaluated with a function that raises an exception"""

        def always_fail():
            raise ValueError("Always fails")

        @smart_args
        def risky_function(*, x=Evaluated(always_fail)):
            return x

        with pytest.raises(ValueError, match="Always fails"):
            risky_function()

    def test_smart_args_complex_scenario(self):
        """test complex scenario with multiple types of arguments"""
        call_count = 0

        def get_id():
            nonlocal call_count
            call_count += 1
            return f"id_{call_count}"

        @smart_args
        def complex_function(
            *, name="default", data=Isolated(), id=Evaluated(get_id), count=0
        ):
            return {"name": name, "data": data, "id": id, "count": count}

        result1 = complex_function()
        assert result1["name"] == "default"
        assert result1["id"] == "id_1"
        assert result1["count"] == 0
        assert call_count == 1

        test_data = {"key": "value"}
        result2 = complex_function(name="test", data=test_data, count=5)
        assert result2["name"] == "test"
        assert result2["data"] == test_data
        assert result2["id"] == "id_2"
        assert result2["count"] == 5
        assert call_count == 2

        assert test_data == {"key": "value"}

    def test_smart_args_error_handling(self):
        """test error handling in smart_args"""

        def error_func():
            raise ValueError("Test error")

        @smart_args
        def function_with_error(*, x=Evaluated(error_func)):
            return x

        with pytest.raises(ValueError, match="Test error"):
            function_with_error()

    def test_smart_args_with_none_values(self):
        """test smart_args with None values"""

        @smart_args
        def none_function(*, x=None, y=Isolated()):
            return x, y

        result = none_function(x=None, y=None)
        assert result == (None, None)

        original_list = None
        result = none_function(y=original_list)
        assert result[1] is None
