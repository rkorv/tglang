import os
import sys

languages = [
    "TGLANG_LANGUAGE_OTHER",
    "TGLANG_LANGUAGE_1S_ENTERPRISE",
    "TGLANG_LANGUAGE_ABAP",
    "TGLANG_LANGUAGE_ACTIONSCRIPT",
    "TGLANG_LANGUAGE_ADA",
    "TGLANG_LANGUAGE_APACHE_GROOVY",
    "TGLANG_LANGUAGE_APEX",
    "TGLANG_LANGUAGE_APPLESCRIPT",
    "TGLANG_LANGUAGE_ASP",
    "TGLANG_LANGUAGE_ASSEMBLY",
    "TGLANG_LANGUAGE_AUTOHOTKEY",
    "TGLANG_LANGUAGE_AWK",
    "TGLANG_LANGUAGE_BASIC",
    "TGLANG_LANGUAGE_BATCH",
    "TGLANG_LANGUAGE_BISON",
    "TGLANG_LANGUAGE_C",
    "TGLANG_LANGUAGE_CLOJURE",
    "TGLANG_LANGUAGE_CMAKE",
    "TGLANG_LANGUAGE_COBOL",
    "TGLANG_LANGUAGE_COFFESCRIPT",
    "TGLANG_LANGUAGE_COMMON_LISP",
    "TGLANG_LANGUAGE_CPLUSPLUS",
    "TGLANG_LANGUAGE_CRYSTAL",
    "TGLANG_LANGUAGE_CSHARP",
    "TGLANG_LANGUAGE_CSS",
    "TGLANG_LANGUAGE_CSV",
    "TGLANG_LANGUAGE_D",
    "TGLANG_LANGUAGE_DART",
    "TGLANG_LANGUAGE_DELPHI",
    "TGLANG_LANGUAGE_DOCKER",
    "TGLANG_LANGUAGE_ELIXIR",
    "TGLANG_LANGUAGE_ELM",
    "TGLANG_LANGUAGE_ERLANG",
    "TGLANG_LANGUAGE_FIFT",
    "TGLANG_LANGUAGE_FORTH",
    "TGLANG_LANGUAGE_FORTRAN",
    "TGLANG_LANGUAGE_FSHARP",
    "TGLANG_LANGUAGE_FUNC",
    "TGLANG_LANGUAGE_GAMS",
    "TGLANG_LANGUAGE_GO",
    "TGLANG_LANGUAGE_GRADLE",
    "TGLANG_LANGUAGE_GRAPHQL",
    "TGLANG_LANGUAGE_HACK",
    "TGLANG_LANGUAGE_HASKELL",
    "TGLANG_LANGUAGE_HTML",
    "TGLANG_LANGUAGE_ICON",
    "TGLANG_LANGUAGE_IDL",
    "TGLANG_LANGUAGE_INI",
    "TGLANG_LANGUAGE_JAVA",
    "TGLANG_LANGUAGE_JAVASCRIPT",
    "TGLANG_LANGUAGE_JSON",
    "TGLANG_LANGUAGE_JULIA",
    "TGLANG_LANGUAGE_KEYMAN",
    "TGLANG_LANGUAGE_KOTLIN",
    "TGLANG_LANGUAGE_LATEX",
    "TGLANG_LANGUAGE_LISP",
    "TGLANG_LANGUAGE_LOGO",
    "TGLANG_LANGUAGE_LUA",
    "TGLANG_LANGUAGE_MAKEFILE",
    "TGLANG_LANGUAGE_MARKDOWN",
    "TGLANG_LANGUAGE_MATLAB",
    "TGLANG_LANGUAGE_NGINX",
    "TGLANG_LANGUAGE_NIM",
    "TGLANG_LANGUAGE_OBJECTIVE_C",
    "TGLANG_LANGUAGE_OCAML",
    "TGLANG_LANGUAGE_OPENEDGE_ABL",
    "TGLANG_LANGUAGE_PASCAL",
    "TGLANG_LANGUAGE_PERL",
    "TGLANG_LANGUAGE_PHP",
    "TGLANG_LANGUAGE_PL_SQL",
    "TGLANG_LANGUAGE_POWERSHELL",
    "TGLANG_LANGUAGE_PROLOG",
    "TGLANG_LANGUAGE_PROTOBUF",
    "TGLANG_LANGUAGE_PYTHON",
    "TGLANG_LANGUAGE_QML",
    "TGLANG_LANGUAGE_R",
    "TGLANG_LANGUAGE_RAKU",
    "TGLANG_LANGUAGE_REGEX",
    "TGLANG_LANGUAGE_RUBY",
    "TGLANG_LANGUAGE_RUST",
    "TGLANG_LANGUAGE_SAS",
    "TGLANG_LANGUAGE_SCALA",
    "TGLANG_LANGUAGE_SCHEME",
    "TGLANG_LANGUAGE_SHELL",
    "TGLANG_LANGUAGE_SMALLTALK",
    "TGLANG_LANGUAGE_SOLIDITY",
    "TGLANG_LANGUAGE_SQL",
    "TGLANG_LANGUAGE_SWIFT",
    "TGLANG_LANGUAGE_TCL",
    "TGLANG_LANGUAGE_TEXTILE",
    "TGLANG_LANGUAGE_TL",
    "TGLANG_LANGUAGE_TYPESCRIPT",
    "TGLANG_LANGUAGE_UNREALSCRIPT",
    "TGLANG_LANGUAGE_VALA",
    "TGLANG_LANGUAGE_VBSCRIPT",
    "TGLANG_LANGUAGE_VERILOG",
    "TGLANG_LANGUAGE_VISUAL_BASIC",
    "TGLANG_LANGUAGE_WOLFRAM",
    "TGLANG_LANGUAGE_XML",
    "TGLANG_LANGUAGE_YAML",
]
language2id = {lang: i for i, lang in enumerate(languages)}


def calc_accuracy(pred, gt):
    assert len(pred) == len(gt)

    correct = 0
    for i in range(len(pred)):
        if pred[i] == gt[i]:
            correct += 1

    return correct, correct / len(pred)


def find_extra_time(time, max_time=0.015):
    extra_time_ids = []
    for i in range(len(time)):
        if time[i] > max_time:
            extra_time_ids.append(i)
    return extra_time_ids


def get_failed_ids(pred):
    failed_ids = []
    for i in range(len(pred)):
        if pred[i].strip() == "":
            failed_ids.append(i)
    return failed_ids


def prepare_gt(paths):
    return [language2id[os.path.basename(os.path.dirname(path))] for path in paths]


def analyse(path_to_csv):
    with open(path_to_csv, "r") as f:
        data = f.readlines()

    data = data[1:]
    data = [line.strip().split(",") for line in data]
    times, pred_labels, files = zip(*data)

    failed_ids = get_failed_ids(pred_labels)
    if len(failed_ids) > 0:
        print("#" * 20 + "  FAILED  " + "#" * 20)
        for i in failed_ids:
            print(f"[{times[i]:.3f}s]: {files[i]}")
        return

    times = [float(t) for t in times]
    pred_labels = [int(l) for l in pred_labels]
    gt = prepare_gt(files)

    correct_num, accuracy = calc_accuracy(pred_labels, gt)
    avg_time = sum([float(t) for t in times]) / len(times)

    print("#" * 20 + "   METRICS   " + "#" * 20)
    print(f"Accuracy: {accuracy: .3f}  [{correct_num}/{len(pred_labels)}]")
    print(f"Avg time: {avg_time: .3f}s [min: {min(times): .3f}s, max: {max(times): .3f}s]")

    extra_time_ids = find_extra_time(times)
    if len(extra_time_ids) > 0:
        print("#" * 20 + " EXTRA TIME " + "#" * 20)
        for i in extra_time_ids:
            print(f"[{times[i]:.3f}s]: {files[i]}")

    print("#" * 20 + "   MISCLASS  " + "#" * 20)
    max_label_len = max([len(l) for l in languages])
    for i in range(len(pred_labels)):
        if pred_labels[i] != gt[i]:
            pred_label_str = languages[pred_labels[i]]
            print(f"[{times[i]:.3f}s] [{pred_label_str:>{max_label_len + 2}}] {files[i]}")


if __name__ == "__main__":
    path_to_csv = sys.argv[1]
    analyse(path_to_csv)
