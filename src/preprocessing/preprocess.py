import ast # abstract syntax tree
import tokenize #  tokenizing Python source code
import io # for in-memory text streams like StringIO 


def remove_comments_and_docstrings(source: str) -> str:
    """
    Remove comments and docstrings from Python source code.
    """
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    tokgen = tokenize.generate_tokens(io_obj.readline)
    for toktype, tok, start, end, line in tokgen:
        if toktype == tokenize.COMMENT:
            continue
        elif toktype == tokenize.STRING:
            if prev_toktype != tokenize.INDENT and last_lineno != start[0]:
                # Likely a docstring → skip it
                continue
        if start[0] > last_lineno:
            last_col = 0
        if start[1] > last_col:
            out += " " * (start[1] - last_col)
        out += tok
        prev_toktype = toktype
        last_col = end[1]
        last_lineno = end[0]
    return out


def normalize_indentation(source: str) -> str:
    """
    Normalize indentation to 4 spaces.
    """
    try:
        tree = ast.parse(source)
        return ast.unparse(tree)  # Python 3.9+ only
    except Exception:
        # If parsing fails, fallback to original
        return source


def preprocess_code(code: str) -> str:
    """
    Apply all preprocessing steps:
      - Remove comments and docstrings
      - Normalize indentation
    """
    code_no_comments = remove_comments_and_docstrings(code)
    code_normalized = normalize_indentation(code_no_comments)
    return code_normalized.strip()


if __name__ == "__main__":
    # Quick test
    raw_code = """
def add(a, b):
    # This function adds two numbers
    \"\"\" Example docstring \"\"\"
    return a+b  # return result
"""
    cleaned = preprocess_code(raw_code)
    print("Before:\n", raw_code)
    print("\nAfter:\n", cleaned)
