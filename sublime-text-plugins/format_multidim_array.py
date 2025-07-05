# Save this file in Sublime Text/Packages/User
#
# add this to your keybindings:
# { "keys": ["ctrl+alt+shift+f"], "command": "format_multidim_array" }
# 
# Use the shortcut above to format a multi-dimensional array following the rules:
# 1) it will format the line where the carat is, provided it is a multidimensional array
# 2) it will format single selected lines, partially, fully, or triple clicked selections (with the carat on the next line)
# 3) it will NOT format the whole file at once
# 4) it will NOT format multiple line selections

import sublime, sublime_plugin, re

# ─── regex to capture indent, head, body ────────────────────────────────────
rx = re.compile(r"^([ \t]*)([^\[\]]+\[)([^\]]*?)\]")

def wrap(indent: str, head: str, body: str, indent_unit: str) -> str:
    if ',' not in body:                       # already single-index
        print("no commas, aborting formatting...")
        return indent + head + body + ']'

    print("Formatting array...")
    parts = [p.strip() for p in body.split(',')]
    body_indent = indent + indent_unit

    def line(pre, txt, comma=False):
        return f"{pre}{txt}{',' if comma else ''} ..."

    lines  = [line(indent, head)]                       # header
    lines += [line(body_indent, p, i < len(parts)-1)    # body items
              for i, p in enumerate(parts)]
    lines.append(indent + ']')                          # closer
    
    # now let's reconstruct the lines with vertical alignment for the '...''
    # first we need the line with the largest width
    largest_width = max(len(e) for e in lines)

    # then we reconstruct the lines aligning the '...'s
    formatted_lines = [
        (e[:-3] + ' ' * (largest_width - len(e) + 3) + '...')
        if e.endswith(' ...') else e           # notice the space before dots ( on purpose!)
        for e in lines
    ]

    return '\n'.join(formatted_lines)

class FormatMultidimArrayCommand(sublime_plugin.TextCommand):
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
