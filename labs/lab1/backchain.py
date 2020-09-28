from production import (
    AND,
    OR,
    NOT,
    PASS,
    FAIL,
    IF,
    THEN,
    match,
    populate,
    simplify,
    variables,
)
from zookeeper import ZOOKEEPER_RULES

from utils import (
    AIStringToPyTemplate,
    AIStringToRegex,
    NoClobberDict,
    ClobberedDictKey,
    AIStringVars,
)

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    tree = OR(hypothesis)
    for rule in rules:
        for c in rule.consequent():
            bindings = match(c, hypothesis)
            if bindings is not None:
                populated_antecedent = populate(rule.antecedent(), bindings)
                if isinstance(populated_antecedent, str):
                    populated_antecedent = OR(populated_antecedent)

                for i, hyp in enumerate(populated_antecedent):
                    sub_tree = backchain_to_goal_tree(rules, hyp)
                    populated_antecedent[i] = sub_tree

                tree.append(populated_antecedent)

    return simplify(tree)


# Here's an example of running the backward chainer - uncomment
# it to see it work:
# print(backchain_to_goal_tree(ZOOKEEPER_RULES, "opus is a penguin"))
