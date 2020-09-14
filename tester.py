import traceback
import os
import tarfile
from io import StringIO


def test_summary(dispindex, ntests):
    return "Test %d/%d" % (dispindex, ntests)


def show_result(testsummary, testcode, correct, got, expected, verbosity):
    if correct:
        if verbosity > 0:
            print("%s: Correct." % testsummary)
        if verbosity > 1:
            print("\t", testcode)
            print()
    else:
        print("%s: Incorrect." % testsummary)
        print("\t", testcode)
        print("Got:     ", got)
        print("Expected:", expected)


def show_exception(testsummary, testcode):
    print("%s: Error." % testsummary)
    print("While running the following test case:")
    print("\t", testcode)
    print("Your code encountered the following error:")
    traceback.print_exc()
    print()


def get_lab_module():
    lab = None

    # Try the easy way first
    try:
        from tests import lab_number

        lab = __import__("lab%s" % lab_number)
    except ImportError:
        pass

    for labnum in range(6):
        try:
            lab = __import__("lab%s" % labnum)
        except ImportError:
            pass

    if lab is None:
        raise ImportError(
            "Cannot find your lab; or, error importing it.  Try loading it by running 'python labN.py' (for the appropriate value of 'N')."
        )

    if not hasattr(lab, "LAB_NUMBER"):
        lab.LAB_NUMBER = 5

    return lab


def run_test(test, lab):
    ans_id, ans_type, attr_name, args = test
    attr = getattr(lab, attr_name)

    if ans_type == "VALUE":
        return attr
    elif ans_type == "FUNCTION":
        return attr(*args)
    else:
        raise Exception(
            "Test Error: Unknown TYPE '%s'.  Please make sure you have downloaded the latest version of the tester script.  If you continue to see this error, contact a TA."
        )


def test_offline(tests_module, verbosity=1):
    test_names = list(tests_module.__dict__.keys())
    test_names.sort()

    tests = [
        (
            x[:-8],
            getattr(tests_module, x),
            getattr(tests_module, "%s_testanswer" % x[:-8]),
            getattr(tests_module, "%s_expected" % x[:-8]),
            "_".join(x[:-8].split("_")[:-1]),
        )
        for x in test_names
        if x[-8:] == "_getargs"
    ]

    ntests = len(tests)
    ncorrect = 0

    for index, (testname, getargs, testanswer, expected, fn_name) in enumerate(tests):
        dispindex = index + 1
        summary = test_summary(dispindex, ntests)

        if getargs == "VALUE":
            ans_type = "VALUE"

            def getargs():
                return getattr(get_lab_module(), testname)

            fn_name = testname
        else:
            ans_type = "FUNCTION"

        try:
            answer = run_test((0, ans_type, fn_name, getargs()), get_lab_module())
            correct = testanswer(answer)
        except Exception:
            show_exception(summary, testname)
            continue

        show_result(summary, testname, correct, answer, expected, verbosity)
        if correct:
            ncorrect += 1

    print("Passed %d of %d tests." % (ncorrect, ntests))
    return ncorrect == ntests


def get_target_upload_filedir():
    cwd = (
        os.getcwd()
    )  # Get current directory.  Play nice with Unicode pathnames, just in case.

    print("Please specify the directory containing your lab.")
    print("Note that all files from this directory will be uploaded!")
    print("Labs should not contain large amounts of data; very-large")
    print("files will fail to upload.")
    print()
    print("The default path is '%s'" % cwd)
    target_dir = input("[%s] >>> " % cwd)

    target_dir = target_dir.strip()
    if target_dir == "":
        target_dir = cwd

    print("Ok, using '%s'." % target_dir)

    return target_dir


def get_tarball_data(target_dir, filename):
    data = StringIO()
    file = tarfile.open(filename, "w|bz2", data)

    print("Preparing the lab directory for transmission...")

    file.add(target_dir)

    print("Done.")
    print()
    print("The following files have been added:")

    for f in file.getmembers():
        print(f.name)

    file.close()

    return data.getvalue()


if __name__ == "__main__":
    import argparse
    import sys

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--lab_dir",
        "-l",
        default="labs/lab0",
        help="path to the unzipped lab directory",
    )
    args = vars(ap.parse_args())

    # Add lab dir to path for importing tests
    sys.path.append(args["lab_dir"])

    import tests as tests_module

    test_offline(tests_module)
