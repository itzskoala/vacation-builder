import re
import markdown


_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #f4f1ec;
    color: #2c2c2c;
    line-height: 1.7;
    padding: 2rem 1rem;
}

.container {
    max-width: 860px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    padding: 3rem 3.5rem;
}

h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: #1a1a2e;
    border-bottom: 3px solid #e8834a;
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
}

h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1a1a2e;
    margin-top: 2.5rem;
    margin-bottom: 0.75rem;
    border-left: 4px solid #e8834a;
    padding-left: 0.75rem;
}

h3 {
    font-size: 1.15rem;
    font-weight: 600;
    color: #333;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}

p { margin-bottom: 1rem; }

ul, ol {
    margin: 0.5rem 0 1rem 1.5rem;
}

li { margin-bottom: 0.3rem; }

a { color: #e8834a; text-decoration: none; }
a:hover { text-decoration: underline; }

blockquote {
    background: #fff8f0;
    border-left: 4px solid #e8834a;
    border-radius: 0 6px 6px 0;
    padding: 0.75rem 1rem;
    margin: 1rem 0;
    color: #555;
    font-style: italic;
}

code {
    background: #f0ede8;
    border-radius: 4px;
    padding: 0.15em 0.4em;
    font-size: 0.9em;
    font-family: "SF Mono", "Fira Code", monospace;
}

pre {
    background: #f0ede8;
    border-radius: 8px;
    padding: 1rem;
    overflow-x: auto;
    margin-bottom: 1rem;
}

pre code { background: none; padding: 0; }

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0 1.5rem;
    font-size: 0.95rem;
}

th {
    background: #1a1a2e;
    color: #fff;
    padding: 0.6rem 0.9rem;
    text-align: left;
}

td {
    padding: 0.55rem 0.9rem;
    border-bottom: 1px solid #e8e4de;
}

tr:nth-child(even) td { background: #faf8f5; }

img {
    max-width: 100%;
    border-radius: 10px;
    margin: 0.75rem 0;
    display: block;
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

hr {
    border: none;
    border-top: 1px solid #e8e4de;
    margin: 2rem 0;
}

strong { color: #1a1a2e; }
"""

_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <style>{css}</style>
</head>
<body>
  <div class="container">
    {body}
  </div>
</body>
</html>
"""


def _extract_title(md_text: str) -> str:
    """Pull the first H1 line as the page title, fallback to generic."""
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Vacation Package"


def convert_md_to_html(md_path: str, html_path: str) -> None:
    """Read a markdown file and write a styled HTML file."""
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br"],
    )

    title = _extract_title(md_text)
    html = _HTML_TEMPLATE.format(title=title, css=_CSS, body=body)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
