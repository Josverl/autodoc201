import contextlib
from functools import cache, lru_cache
from pathlib import Path
from typing import List
import pytest

from bs4 import BeautifulSoup
import difflib
import requests

import unicodedata


def normalize_and_clean(text):
    # Normalize the text to NFC form
    normalized_text = unicodedata.normalize("NFC", text)
    # Remove specific characters
    cleaned_text = normalized_text.replace("\uf0c1", "").replace("¶", "")
    return cleaned_text


def read_html(file: Path):
    with open(file, "r", encoding="utf-8") as fp:
        return fp.read()


@lru_cache
def fetch_html(url: str):
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    response.encoding = "utf-8"  # Set the encoding to utf-8
    return normalize_and_clean(response.text)


def extract_element_text(html_content, selector):
    soup = BeautifulSoup(html_content, "html.parser")
    element = soup.select_one(selector)
    return normalize_and_clean(element.get_text()) if element else ""


# things to ignore in the diff
LINE_JUNK = {
    "\n",
    "\t",
    "This is the v1.23.0 version of the MicroPython",
    "documentation. The latest",
    "development version of this page may be more current.",
    "This is the documentation for the latest development branch of",
    "MicroPython and may refer to features that are not available in released",
    "versions.",
    "If you are looking for the documentation for a specific release, use",
    "the drop-down menu on the left and select the desired version.",
}

# things to ignore in the diff
LINE_MIP_TIP = {
    "Tip",
    "This is a python-stdlib module from the micropython-lib repository.",
    "It can be installed to a MicroPython board using:",
}


def ignore_version_notice(diff_lines: List[str]):
    return [
        l
        for l in diff_lines
        if l[0] not in " ?" and l[1:].strip() != "" and l[1:].strip() not in LINE_JUNK
    ]


def ignore_mip_tip(diff_lines: List[str]):
    return [
        l
        for l in diff_lines
        if not (
            l[1:].strip() in LINE_MIP_TIP
            or l[2:].startswith("mpremote mip install")
            or l[2:].startswith(
                "Source: https://github.com/micropython/micropython-lib/tree/master"
            )
        )
    ]


def ignore_assignments(diff_lines):
    """
    Ignore lines that are assignments of the form `+ x = ...`
    but only if the line is also present in the opposite form without the value.

    """
    r2 = diff_lines.copy()
    for l in diff_lines:
        if l.startswith("+ ") and "=" in l:
            partial = l.split("=")[0].strip()
            opposite = f"- {partial[2:]}"
            if opposite in r2:
                r2.remove(l)
                r2.remove(opposite)
    return r2


def find_title(lines: List[str]):
    """Find the title of the module in the documentation
    assumes that the title is the first line that is not indented or empty
    and that the title is separated from the module name by a dash or en-dash::

        foo - Description of foo

    """
    title_line = module_name = title = ""
    for line in lines:
        if line and not line.startswith(" "):
            title_line = line
            break
    # BEWARE : "–" is not the same as "-" (en-dash vs hyphen)
    if title_line:
        for sep in ["–", "-"]:
            if sep in title_line:
                module_name, title = title_line.split(sep, 1)
                module_name = module_name.strip()
                title = title.strip()
                break

    return module_name, title, title_line


IGNORE_HEADINGS = {
    "- Functions",
    "- Classes",
    "- Constants",
    "- Exceptions",
    "- Methods",
    "- Constructor",
}


def ignore_known_headings(diff_lines: List[str]):
    return [l for l in diff_lines if l not in IGNORE_HEADINGS]


def ignore_moves(result):
    r2 = result.copy()
    for l in result:
        opposite = f"- {l[2:]}" if l.startswith("+ ") else f"+ {l[2:]}"
        if opposite in r2:
            with contextlib.suppress(ValueError):
                r2.remove(l)
            with contextlib.suppress(ValueError):
                r2.remove(opposite)
    return r2


def allow_new_data_assignments(diff_lines: List[str]):
    return [
        l
        for l in diff_lines
        if not (
            l.startswith("+ ")
            and "=" in l
            # and l[2:].strip().startswith(("b'", "u'", "f'", "r'", '"', "'"))
        )
    ]


def allow_different_parameters(diff_lines: List[str]):
    """
    functions, methods and classes can have different parameters in the local and web versions
    Does not deal with the case where the parameters are in a separate line ....
    """
    r2 = diff_lines.copy()
    for l in diff_lines:
        if "(" in l:
            partial = l.split("(")[0].strip()
            opposite = f"{opp_change(l)} {partial[2:]}"
            if opposite in r2:
                with contextlib.suppress(ValueError):
                    r2.remove(l)
                with contextlib.suppress(ValueError):
                    r2.remove(opposite)
            elif l2 := diff_startswith(r2, f"{opposite}("):
                # also remove if the params dont match
                with contextlib.suppress(ValueError):
                    r2.remove(l)
                with contextlib.suppress(ValueError):
                    r2.remove(l2)

    return r2


def allow_omit_class_different_parameters(diff_lines: List[str]):
    """
    functions, methods and classes can have different parameters in the local and web versions
    Does not deal with the case where the parameters are in a separate line ....
    """
    r2 = diff_lines.copy()
    for l in diff_lines:
        if "(" in l:
            partial = l.split("(")[0].strip()
            if "." in partial:
                partial = "- " + partial.split(".", 1)[1]
            opposite = f"{opp_change(l)} {partial[2:]}"
            if opposite in r2:
                with contextlib.suppress(ValueError):
                    r2.remove(l)
                with contextlib.suppress(ValueError):
                    r2.remove(opposite)
            elif l2 := diff_startswith(r2, f"{opposite}("):
                # also remove if the params dont match
                with contextlib.suppress(ValueError):
                    r2.remove(l)
                with contextlib.suppress(ValueError):
                    r2.remove(l2)
    return r2


def diff_startswith(diff_lines: List[str], prefix: str):
    for l in diff_lines:
        if l.startswith(prefix):
            return l
    return None


def opp_change(l):
    # + -> - and - -> +
    return "+" if l[0] == "-" else "-"


def compare_html(file1: Path, url: str, ignore_title=True):
    # this is the most relevant section of a Sphinx-generated HTML page
    # that contains the actual documentation content

    selector = "body > div > section > div > div > div.document"
    html_web = fetch_html(url)
    html_local = read_html(file1)

    lines_web = (extract_element_text(html_web, selector)).splitlines()
    # only skip local
    lines_local = (extract_element_text(html_local, selector)).splitlines()
    # write to a file for debugging
    with open("page_web.txt", "w") as f:
        f.write("\n".join(lines_web))
    with open("page_local.txt", "w") as f:
        f.write("\n".join(lines_local))

    module_name, title, title_line = find_title(lines_local)

    diff = difflib.ndiff(
        lines_web,
        lines_local,
    )

    result = ignore_version_notice(list(diff))
    result = ignore_mip_tip(result)

    # There are fewer headings in the autoapimodule ( TODO: could be added in the template )
    result = ignore_known_headings(result)

    # remove all the lines that appear with both a + and a - prefix (they are line-moves / re-orderings)
    result = ignore_moves(result)
    # the stubs have more precise parameter information, so likely to be different
    result = allow_different_parameters(result)
    result = allow_omit_class_different_parameters(result)
    # the subs have values for data, so likely to be different
    result = ignore_assignments(result)
    # there are some assignments that are not present in the web version
    result = allow_new_data_assignments(result)

    if ignore_title:
        # The stubs have the title of the docpage in the first line, so we can ignore it
        for t_diff in [f"+ {title.capitalize()}.", f"+ {title}"]:
            if t_diff in result:
                result.remove(t_diff)
                break
    return result


def simularity(file1: Path, url: str, ignore_title=True):
    # this is the most relevant section of a Sphinx-generated HTML page
    # that contains the actual documentation content

    selector = "body > div > section > div > div > div.document"
    html_web = fetch_html(url)
    html_local = read_html(file1)

    lines_web = (extract_element_text(html_web, selector)).splitlines()
    # only skip local
    lines_local = (extract_element_text(html_local, selector)).splitlines()

    sim = difflib.SequenceMatcher(None, lines_web, lines_local).ratio()
    return sim


from pathlib import Path

fldr = Path("docs/library")

autoapifiles = []
for f in fldr.glob("*.rst"):
    with f.open() as fp:
        content = fp.read()
    if "autoapi" in content:
        autoapifiles.append(f.relative_to(Path("docs")).with_suffix("").as_posix())


@pytest.mark.parametrize(
    "page",
    autoapifiles,
)
def test_library_page(page: str):
    version = "v1.23.0"
    local_page = Path(f"D:\\mypython\\autodoc201\\docs\\build\\html\\{page}.html").resolve()
    url = f"https://docs.micropython.org/en/{version}/{page}.html"
    diff = compare_html(local_page, url, ignore_title=True)
    # for now we only care that nothing is missing
    diff = [l for l in diff if l.startswith("- ")]

    if diff:
        print(f"Diff for {page}:")
        for line in diff:
            print(line)
    newline = "\n"
    assert len(diff) < 10, f"Diff= {newline.join(diff)}"
    # # Not exactly the same
    # sim = simularity(local_page, url)
    # print(f"Simularity for {page}: {sim}")
    # assert sim > 0.8, f"Simularity for {page} is only {sim}"
