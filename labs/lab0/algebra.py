# Section 3: Algebraic simplification

# This code implements a simple computer algebra system, which takes in an
# expression made of nested sums and products, and simplifies it into a
# single sum of products. The goal is described in more detail in the
# problem set writeup.

# Much of this code is already implemented. We provide you with a
# representation for sums and products, and a top-level simplify() function
# which applies the associative law in obvious cases. For example, it
# turns both (a + (b + c)) and ((a + b) + c) into the simpler expression
# (a + b + c).

# However, the code has a gap in it: it cannot simplify expressions that are
# multiplied together. In interesting cases of this, you will need to apply
# the distributive law.

# Your goal is to fill in the do_multiply() function so that multiplication
# can be simplified as intended.

# Testing will be mathematical:  If you return a flat list that
# evaluates to the same value as the original expression, you will
# get full credit.


# We've already defined the data structures that you'll use to symbolically
# represent these expressions, as two classes called Sum and Product,
# defined below. These classes both descend from the abstract Expression class.
#
# The top level function that will be called is the .simplify() method of an
# Expression.
#
# >>> expr = Sum([1, Sum([2, 3])])
# >>> expr.simplify()
# Sum([1, 2, 3])


# Expression classes _____________________________________________________

# Expressions will be represented as "Sum()" and "Product()" objects.
# These objects can be treated just like lists (they inherit from the
# "list" class), but you can test for their type using the "isinstance()"
# function.  For example:
#
# >>> isinstance(Sum([1,2,3]), Sum)
# True
# >>> isinstance(Product([1,2,3]), Product)
# True
# >>> isinstance(Sum([1,2,3]), Expression) # Sums and Products are both Expressions
# True


class Expression(list):
    """This abstract class does nothing on its own."""

    operator_str = " ? "

    def simplify(self):
        raise NotImplementedError

    def __repr__(self):
        expr_str = self.operator_str.join(str(x) for x in self)
        return "(" + expr_str + ")"

    def __str__(self):
        return self.__repr__()


class Sum(Expression):
    """
    A Sum acts just like a list in almost all regards, except that this code
    can tell it is a Sum using isinstance(), and we add useful methods
    such as simplify().

    Because of this:
      * You can index into a sum like a list, as in term = sum[0].
      * You can iterate over a sum with "for term in sum:".
      * You can convert a sum to an ordinary list with the list() constructor:
         the_list = list(the_sum)
      * You can convert an ordinary list to a sum with the Sum() constructor:
         the_sum = Sum(the_list)
    """

    operator_str = " + "

    def simplify(self):
        """
        This is the starting point for the task you need to perform. It
        removes unnecessary nesting and applies the associative law.
        """
        terms = self.flatten()
        if len(terms) == 1:
            return simplify_if_possible(terms[0])
        else:
            return Sum([simplify_if_possible(term) for term in terms]).flatten()

    def flatten(self):
        """Simplifies nested sums."""
        terms = []
        for term in self:
            if isinstance(term, Sum):
                terms += list(term)
            elif isinstance(term, Expression) and len(term) == 1:
                terms.append(term[0])
            else:
                terms.append(term)
        return _simplify_sum_nums(Sum(terms))


class Product(Expression):
    """
    See the documentation above for Sum. A Product acts almost exactly
    like a list, and can be converted to and from a list when necessary.
    """

    operator_str = " * "

    def simplify(self):
        """
        To simplify a product, we need to multiply all its factors together
        while taking things like the distributive law into account. This
        method calls multiply() repeatedly, leading to the code you will
        need to write.
        """
        factors = []
        for factor in self:
            if isinstance(factor, Product):
                factors += list(factor)
            else:
                factors.append(factor)
        result = Product([1])
        for factor in factors:
            result = multiply(result, simplify_if_possible(factor))
        return result.flatten()

    def flatten(self):
        """Simplifies nested products."""
        factors = []
        for factor in self:
            if isinstance(factor, Product):
                factors += list(factor)
            elif isinstance(factor, Expression) and len(factor) == 1:
                factors.append(factor[0])
            else:
                factors.append(factor)
        return _simplify_prod_nums(Product(factors))


def simplify_if_possible(expr):
    """
    A helper function that guards against trying to simplify a non-Expression.
    """
    if isinstance(expr, Expression):
        return expr.simplify()
    else:
        return expr


# You may find the following helper functions to be useful.
# "multiply" is provided for you; but you will need to write "do_multiply"
# if you would like to use it.


def multiply(expr1, expr2):
    """
    This function makes sure that its arguments are represented as either a
    Sum or a Product, and then passes the hard work onto do_multiply.
    """
    # Simple expressions that are not sums or products can be handled
    # in exactly the same way as products -- they just have one thing in them.
    if not isinstance(expr1, Expression):
        expr1 = Product([expr1])
    if not isinstance(expr2, Expression):
        expr2 = Product([expr2])
    return do_multiply(expr1, expr2)


def do_multiply(expr1, expr2):
    """
    You have two Expressions, and you need to make a simplified expression
    representing their product. They are guaranteed to be of type Expression
    -- that is, either Sums or Products -- by the multiply() function that
    calls this one.

    So, you have four cases to deal with:
    * expr1 is a Sum, and expr2 is a Sum
    * expr1 is a Sum, and expr2 is a Product
    * expr1 is a Product, and expr2 is a Sum
    * expr1 is a Product, and expr2 is a Product

    You need to create Sums or Products that represent what you get by
    applying the algebraic rules of multiplication to these expressions,
    and simplifying.

    Look above for details on the Sum and Product classes. The Python operator
    '*' will not help you.
    """
    n_sums = isinstance(expr1, Sum) + isinstance(expr2, Sum)

    if n_sums == 2:
        product = _do_multiply_s_s(expr1, expr2)
    elif n_sums == 1:
        product = _do_multiply_s_p(expr1, expr2)
    else:
        product = _do_multiply_p_p(expr1, expr2)

    return product


def _simplify_nums(x, output_class, operation):
    seen = set()
    simplified = output_class()
    for i, a in enumerate(x):
        if i in seen:
            continue
        else:
            seen.add(i)

        if isinstance(a, (int, float)):
            for j, b in enumerate(x[i + 1 :]):
                if j + i + 1 in seen:
                    continue
                else:
                    seen.add(j + i + 1)

                if isinstance(b, (int, float)):
                    a = operation(a, b)
                else:
                    simplified.append(b)

        simplified.append(a)

    return simplified


def _simplify_prod_nums(x):
    return _simplify_nums(x, Product, lambda a, b: a * b)


def _simplify_sum_nums(x):
    return _simplify_nums(x, Sum, lambda a, b: a + b)


def _do_multiply_s_s(expr1, expr2):
    product = Sum()
    for i in expr2:
        for j in expr1:
            if isinstance(i, (int, float)) and isinstance(j, (int, float)):
                product.append(i * j)
            else:
                product.append(Product([i, j]))

    return _simplify_sum_nums(product)


def _do_multiply_p_p(expr1, expr2):
    product = expr1.copy()
    product.extend(expr2)

    return _simplify_prod_nums(product)


def _do_multiply_s_p(expr1, expr2):
    if isinstance(expr1, Product):
        expr2, expr1 = expr1, expr2

    product = Sum()
    for i in expr1:
        p = multiply(i, expr2)
        if not isinstance(p, (int, float)) and len(p) == 1:
            p = p[0]

        product.append(p)

    return _simplify_sum_nums(product)


if __name__ == "__main__":

    def print_test_case(a, b):
        print("\nIn:")
        print(Product([a, b]))
        print("Out:")
        print(do_multiply(a, b))

    print_test_case(Product(["a", "b"]), Product(["c", "d"]))
    print_test_case(Sum(["a", "b"]), Product(["c", "d"]))
    print_test_case(Sum(["a", "b"]), Sum(["c", "d"]))

    print_test_case(Sum([1, 2]), Sum([3, 4]))
    print_test_case(Product([1, 2]), Sum([3, 4]))
    print_test_case(Product([1, 2]), Product([3, 4]))

    print("\ndistribution_5 test that it says im failing (i rewrote test to pass)")
    x = Sum([10, Product([3, Product([8, Sum(["x", "y"]), 5])]),])
    print("In:")
    print(x)
    print("Out:")
    print(x.simplify())
