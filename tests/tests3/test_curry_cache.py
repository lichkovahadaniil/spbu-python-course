import pytest
from project.task3.curry_cache import curry_explicit, uncurry_explicit, deco_cache


class TestCurryExplicit:
    """tests for curry_explicit"""

    def test_curry_basic_functionality(self):
        """test basic functionality of currying"""

        def add_three(x, y, z):
            return x + y + z

        curried = curry_explicit(add_three, 3)
        result = curried(1)(2)(3)
        assert result == 6

    def test_curry_arity_zero(self):
        """test currying with arity 0"""

        def get_constant():
            return 42

        curried = curry_explicit(get_constant, 0)
        result = curried()
        assert result == 42

    def test_curry_arity_one(self):
        """test currying with arity 1"""

        def square(x):
            return x * x

        curried = curry_explicit(square, 1)
        result = curried(5)
        assert result == 25

    def test_curry_negative_arity(self):
        """test error when arity is negative"""

        def dummy_func():
            pass

        with pytest.raises(ValueError, match="The arity must be greater, than 0"):
            curry_explicit(dummy_func, -1)

    def test_curry_too_many_args(self):
        """test error when too many arguments are passed"""

        def add_two(x, y):
            return x + y

        curried = curry_explicit(add_two, 2)

        with pytest.raises(TypeError, match="Incorrect quantity of arguments"):
            curried(1, 2, 3)

    def test_curry_lambda_function(self):
        """test currying of lambda function"""
        curried = curry_explicit((lambda x, y, z: f"<{x},{y},{z}>"), 3)
        result = curried(123)(456)(562)
        assert result == "<123,456,562>"

    def test_curry_with_print(self):
        """test currying of print function"""
        curried = curry_explicit(print, 2)
        result = curried(1)(2)
        assert result is None

    def test_curry_partial_application(self):
        """test partial application"""

        def multiply_four(a, b, c, d):
            return a * b * c * d

        curried = curry_explicit(multiply_four, 4)
        partial = curried(2)(3)
        result = partial(4)(5)
        assert result == 120

    def test_curry_with_different_types(self):
        """test currying with different types of data"""

        def concat_strings(a, b, c):
            return f"{a}{b}{c}"

        curried = curry_explicit(concat_strings, 3)
        result = curried("Hello")(" ")("World")
        assert result == "Hello World"


class TestUncurryExplicit:
    """tests for uncurry_explicit"""

    def test_uncurry_basic_functionality(self):
        """test basic functionality of uncurry"""

        def add_three(x, y, z):
            return x + y + z

        curried = curry_explicit(add_three, 3)
        uncurried = uncurry_explicit(curried, 3)
        result = uncurried(1, 2, 3)
        assert result == 6

    def test_uncurry_arity_zero(self):
        """test uncurry with arity 0"""

        def get_constant():
            return 42

        curried = curry_explicit(get_constant, 0)
        uncurried = uncurry_explicit(curried, 0)
        result = uncurried()
        assert result() == 42

    def test_uncurry_arity_one(self):
        """test uncurry with arity 1"""

        def square(x):
            return x * x

        curried = curry_explicit(square, 1)
        uncurried = uncurry_explicit(curried, 1)
        result = uncurried(5)
        assert result == 25

    def test_uncurry_negative_arity(self):
        """test error when arity is negative"""

        def dummy_func():
            pass

        with pytest.raises(ValueError, match="The arity must be greater, than 0"):
            uncurry_explicit(dummy_func, -1)

    def test_uncurry_wrong_number_of_args(self):
        """test error when wrong number of arguments are passed"""

        def add_two(x, y):
            return x + y

        curried = curry_explicit(add_two, 2)
        uncurried = uncurry_explicit(curried, 2)

        with pytest.raises(TypeError, match="Incorrect quantity of arguments"):
            uncurried(1, 2, 3)

        with pytest.raises(TypeError, match="Incorrect quantity of arguments"):
            uncurried(1)

    def test_uncurry_lambda_function(self):
        """test uncurry with lambda function"""
        curried = curry_explicit((lambda x, y, z: f"<{x},{y},{z}>"), 3)
        uncurried = uncurry_explicit(curried, 3)
        result = uncurried(123, 456, 562)
        assert result == "<123,456,562>"

    def test_curry_uncurry_roundtrip(self):
        """test that curry -> uncurry returns the original functionality"""

        def original_func(a, b, c, d):
            return a + b * c - d

        curried = curry_explicit(original_func, 4)
        uncurried = uncurry_explicit(curried, 4)

        args = (10, 2, 3, 5)
        original_result = original_func(*args)
        uncurried_result = uncurried(*args)
        assert original_result == uncurried_result == 11


class TestDecoCache:
    """tests for deco_cache"""

    def test_cache_basic_functionality(self):
        """test basic functionality of caching"""
        call_count = 0

        @deco_cache(2)
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count == 1

        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count == 1

    def test_cache_with_different_args(self):
        """test caching with different arguments"""
        call_count = 0

        @deco_cache(3)
        def add_numbers(x, y):
            nonlocal call_count
            call_count += 1
            return x + y

        assert add_numbers(1, 2) == 3
        assert add_numbers(3, 4) == 7
        assert add_numbers(1, 2) == 3
        assert call_count == 2

    def test_cache_with_kwargs(self):
        """test caching with named arguments"""
        call_count = 0

        @deco_cache(2)
        def multiply(x, y=1):
            nonlocal call_count
            call_count += 1
            return x * y

        assert multiply(5, 2) == 10
        assert multiply(5, 2) == 10
        assert call_count == 1

    def test_cache_limit(self):
        """test cache limit"""
        call_count = 0

        @deco_cache(2)
        def simple_func(x):
            nonlocal call_count
            call_count += 1
            return x

        simple_func(1)
        simple_func(2)
        assert call_count == 2

        simple_func(3)
        assert call_count == 3

        simple_func(1)
        assert call_count == 4

    def test_cache_zero_limit(self):
        """test caching with limit 0 (caching disabled)"""
        call_count = 0

        @deco_cache(0)
        def no_cache_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert no_cache_func(5) == 10
        assert no_cache_func(5) == 10
        assert call_count == 2

    def test_cache_with_mutable_objects(self):
        """test caching with mutable objects"""
        call_count = 0

        @deco_cache(2)
        def process_list(lst):
            nonlocal call_count
            call_count += 1
            return sum(lst)

        list1 = [1, 2, 3]
        list2 = [1, 2, 3]

        result1 = process_list(list1)
        result2 = process_list(list2)

        assert result1 == 6
        assert result2 == 6
        assert call_count == 1

    def test_cache_with_dicts(self):
        """test caching with dictionaries"""
        call_count = 0

        @deco_cache(2)
        def process_dict(d):
            nonlocal call_count
            call_count += 1
            return d.get("value", 0)

        dict1 = {"value": 42}
        dict2 = {"value": 42}

        result1 = process_dict(dict1)
        result2 = process_dict(dict2)

        assert result1 == 42
        assert result2 == 42
        assert call_count == 1

    def test_cache_with_sets(self):
        """test caching with sets"""
        call_count = 0

        @deco_cache(2)
        def process_set(s):
            nonlocal call_count
            call_count += 1
            return len(s)

        set1 = {1, 2, 3}
        set2 = {1, 2, 3}

        result1 = process_set(set1)
        result2 = process_set(set2)

        assert result1 == 3
        assert result2 == 3
        assert call_count == 1

    def test_cache_complex_args(self):
        """test caching with complex arguments"""
        call_count = 0

        @deco_cache(3)
        def complex_function(x, y=1, z=None):
            nonlocal call_count
            call_count += 1
            return x + y + (z or 0)

        assert complex_function(1) == 2
        assert complex_function(1, 2) == 3
        assert complex_function(1, 2, 3) == 6
        assert complex_function(1) == 2
        assert call_count == 3

    def test_cache_with_none_values(self):
        """test caching with None values"""
        call_count = 0

        @deco_cache(2)
        def handle_none(x, y=None):
            nonlocal call_count
            call_count += 1
            return x if y is None else x + y

        assert handle_none(5) == 5
        assert handle_none(5) == 5
        assert handle_none(5, None) == 5
        assert call_count == 2

    def test_cache_with_empty_containers(self):
        """test caching with empty containers"""
        call_count = 0

        @deco_cache(3)
        def process_empty(lst, dct, st):
            nonlocal call_count
            call_count += 1
            return len(lst) + len(dct) + len(st)

        assert process_empty([], {}, set()) == 0
        assert process_empty([], {}, set()) == 0
        assert call_count == 1

    def test_cache_lru_behavior(self):
        """test LRU behavior of cache"""
        call_count = 0

        @deco_cache(2)
        def simple_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        simple_func(1)
        simple_func(2)

        simple_func(3)

        simple_func(1)

        simple_func(3)

        assert call_count == 4
