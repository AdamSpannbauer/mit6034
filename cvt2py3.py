import re
import difflib

TRANSLATIONS = {
    "xmlrpclib": "xmlrpc",
    r"print (.*)": r"print(\1)",
    "print$`": "print()",
    "raw_input`": "input",
    "xrange`": "range",
    r"raise (\w+), (.+)$": r"raise \1(\2)",
    r"apply\((\w+), (\w+)\)": r"\1(*\2)",
}

# Use as `for find, replace in RE_TRANSLATIONS`
RE_TRANSLATIONS = (
    (re.compile(k, flags=re.MULTILINE), v) for k, v in TRANSLATIONS.items()
)


def cvt2py3(text):
    # lines = text.split("\n")
    # for line in lines:
    #     for find, replace in RE_TRANSLATIONS:
    #         line = find.sub(replace, line)

    # return "\n".join(lines)

    for find, replace in RE_TRANSLATIONS:
        text = find.sub(replace, text)

    return text


def file_cvt2py3(file_path, output_file_path=None, display_diff=True):
    if output_file_path is None:
        output_file_path = file_path

    with open(file_path, "r") as f:
        py2_txt = f.read()

    py3_txt = cvt2py3(py2_txt)

    if display_diff:
        diff = difflib.unified_diff(py2_txt.split("\n"), py3_txt.split("\n"))
        for text in diff:
            print(text)

    with open(output_file_path, "w") as f:
        f.write(py3_txt)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        "-i",
        help="file path to python 2 code to convert to py3",
        required=True,
    )
    ap.add_argument(
        "--output",
        "-o",
        help="file path to outputted python 3 code (defaults to input path)",
        required=False,
    )
    args = vars(ap.parse_args())

    file_cvt2py3(args["input"], args["output"])
