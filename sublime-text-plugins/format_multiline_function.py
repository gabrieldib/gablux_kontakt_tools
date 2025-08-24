import sublime, sublime_plugin, re

# ─── regex to capture indent, head, body ────────────────────────────────────
rx = re.compile(r"^([ \t]*)([^\(\)]+\()([^\)]*?)\)")

# --- helper ---------------------------------------------------------------
def split_top_level(s: str):
    """Return a list of items separated by commas *only at depth 0*."""
    parts, buf, depth = [], [], 0
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth = max(0, depth - 1)
        elif ch == ',' and depth == 0:
            parts.append(''.join(buf).strip())
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    parts.append(''.join(buf).strip())
    return parts

def wrap(indent: str, head: str, body: str, indent_unit: str) -> str:
    if ',' not in body:                       # already single-index
        print("no commas, aborting formatting...")
        return indent + head + body + ']'

    print("Formatting array...")
    parts = split_top_level(body)
    body_indent = indent + indent_unit

    def line(pre, txt, comma=False):
        return f"{pre}{txt}{',' if comma else ''} ..."

    lines  = [line(indent, head)]                       # header
    lines += [line(body_indent, p, i < len(parts)-1)    # body items
              for i, p in enumerate(parts)]
    lines.append(indent + ')')                          # closer
    
    # now let's reconstruct the lines with vertical alignment for the '...''
    # first we need the line with the largest width
    largest_width = max(len(e) for e in lines)

    # then we reconstruct the lines aligning the '...'s
    formatted_lines = [
        (e[:-3] + ' ' * (largest_width - len(e)) + ' ...')
        if e.endswith(' ...') else e           # notice the space before dots ( on purpose!)
        for e in lines
    ]

    return '\n'.join(formatted_lines)

class FormatMultilineFunctionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("Running KSP format MD array")
        view = self.view
        reg  = view.sel()[0]                      # first caret / selection

        # ---- determine indent unit from view settings ---------------------
        sett = view.settings()
        if sett.get("translate_tabs_to_spaces"):
            indent_unit = " " * int(sett.get("tab_size", 4))
        else:
            indent_unit = "\t"

        # ---- reject only real multi-line selections ------------------------
        if not reg.empty():
            row_start = view.rowcol(reg.begin())[0]
            row_end   = view.rowcol(reg.end() - 1)[0]
            if row_start != row_end:
                sublime.status_message("We don't process multi-line selections")
                return

        # ---- grab the physical line and transform it ----------------------
        line_region = view.line(reg)
        line_text   = view.substr(line_region)
        print(f'Processing line text: {line_text}')
        new_text    = rx.sub(
            lambda m: wrap(*m.groups(), indent_unit),
            line_text,
            count=1
        )
        view.replace(edit, line_region, new_text)
