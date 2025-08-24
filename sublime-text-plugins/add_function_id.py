import sublime
import sublime_plugin
import os, time, hashlib, json, re

def read_dict():
    file_path = os.path.join(sublime.packages_path(), "User", "hashed_functions_dB.json")
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_dict(data):
    file_path = os.path.join(sublime.packages_path(), "User", "hashed_functions_dB.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def generate_function_id(function_name):
    timestamp = str(time.time())
    unique_string = function_name + "_" + timestamp
    hash_object = hashlib.sha256(unique_string.encode())
    return hash_object.hexdigest()[:6]  # 6-char hash

class AddFunctionIdCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        full_region = sublime.Region(0, view.size())
        content = view.substr(full_region)
        lines = content.splitlines()
        file_path = view.file_name()
        file_name = os.path.basename(file_path) if file_path else "Untitled"
        hashed_db = read_dict()

        modified = False  # track if we changed anything

        for index, line in enumerate(lines):
            function_match = re.match(r"^function\s+([a-zA-Z_][a-zA-Z0-9_]*)", line)
            if not function_match:
                continue

            function_name = function_match.group(1)

            # Check if it's already hashed — starts with fn_ and has a 6-char hex
            already_hashed = re.match(r"^fn_[a-f0-9]{6}_.+", function_name)

            if already_hashed:
                if function_name in hashed_db:
                    db_entry = hashed_db[function_name]
                    if db_entry["function_original_file"] == file_name:
                        print(f"Skipping already-processed function: {function_name}")
                        continue  # Skip this function
                else:
                    print(f"Warning: hashed function found but not in DB: {function_name}")
                    continue  # skip without adding to DB

            # Generate unique ID
            hashed_id = generate_function_id(function_name)
            hashed_name = f"fn_{hashed_id}_{function_name}"

            while hashed_name in hashed_db:
                hashed_id = generate_function_id(function_name)
                hashed_name = f"fn_{hashed_id}_{function_name}"
                print("Hash collision, regenerated:", hashed_name)

            # Update line in file
            new_line = f"function {hashed_name}"
            line_region = view.line(view.text_point(index, 0))
            view.replace(edit, line_region, new_line)
            modified = True

            # Save to DB
            hashed_db[hashed_name] = {
                "original_name": function_name,
                "creation_timestamp": str(time.time()),
                "function_original_file": file_name
            }

            print(f"Function renamed: {function_name} → {hashed_name}")

        report_lines = []

        if modified:
            write_dict(hashed_db)
            view.run_command("save")

            report_lines.append(f"🔧 Updated file: {file_name}")
            report_lines.append("📌 Hashed functions added:")
            for key, entry in hashed_db.items():
                if entry["function_original_file"] == file_name:
                    report_lines.append(f"  - {key} (from {entry['original_name']})")
        else:
            report_lines.append(f"✅ No changes made to '{file_name}' — all functions already processed.")

        report = "\n".join(report_lines)

        # Show in dialog or output panel depending on length
        if len(report_lines) <= 10:
            sublime.message_dialog(report)
        else:
            self.show_output_panel(report)

    def show_output_panel(self, content):
        window = self.view.window()
        panel = window.create_output_panel("function_id_report")
        panel.run_command("append", {"characters": content})
        window.run_command("show_panel", {"panel": "output.function_id_report"})
