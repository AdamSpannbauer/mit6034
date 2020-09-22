from production import IF, AND, THEN, FAIL, OR

## ZOOKEEPER RULES
ZOOKEEPER_RULES = (
    IF(AND("(?x) has hair"), THEN("(?x) is a mammal")),  # Z1
    IF(AND("(?x) gives milk"), THEN("(?x) is a mammal")),  # Z2
    IF(AND("(?x) has feathers"), THEN("(?x) is a bird")),  # Z3
    IF(AND("(?x) flies", "(?x) lays eggs"), THEN("(?x) is a bird")),  # Z4
    IF(AND("(?x) is a mammal", "(?x) eats meat"), THEN("(?x) is a carnivore")),  # Z5
    IF(
        AND(
            "(?x) is a mammal",  # Z6
            "(?x) has pointed teeth",
            "(?x) has claws",
            "(?x) has forward-pointing eyes",
        ),
        THEN("(?x) is a carnivore"),
    ),
    IF(AND("(?x) is a mammal", "(?x) has hoofs"), THEN("(?x) is an ungulate")),  # Z7
    IF(AND("(?x) is a mammal", "(?x) chews cud"), THEN("(?x) is an ungulate")),  # Z8
    IF(
        AND("(?x) is a carnivore", "(?x) has tawny color", "(?x) has dark spots"),  # Z9
        THEN("(?x) is a cheetah"),
    ),
    IF(
        AND(
            "(?x) is a carnivore",  # Z10
            "(?x) has tawny color",
            "(?x) has black stripes",
        ),
        THEN("(?x) is a tiger"),
    ),
    IF(
        AND(
            "(?x) is an ungulate",  # Z11
            "(?x) has long legs",
            "(?x) has long neck",
            "(?x) has tawny color",
            "(?x) has dark spots",
        ),
        THEN("(?x) is a giraffe"),
    ),
    IF(
        AND(
            "(?x) is an ungulate",  # Z12
            "(?x) has white color",
            "(?x) has black stripes",
        ),
        THEN("(?x) is a zebra"),
    ),
    IF(
        AND(
            "(?x) is a bird",  # Z13
            "(?x) does not fly",
            "(?x) has long legs",
            "(?x) has long neck",
            "(?x) has black and white color",
        ),
        THEN("(?x) is an ostrich"),
    ),
    IF(
        AND(
            "(?x) is a bird",  # Z14
            "(?x) does not fly",
            "(?x) swims",
            "(?x) has black and white color",
        ),
        THEN("(?x) is a penguin"),
    ),
    IF(
        AND("(?x) is a bird", "(?x) is a good flyer"),  # Z15
        THEN("(?x) is an albatross"),
    ),
)


ZOO_DATA = (
    "tim has feathers",
    "tim is a good flyer",
    "mark flies",
    "mark does not fly",
    "mark lays eggs",
    "mark swims",
    "mark has black and white color",
)
