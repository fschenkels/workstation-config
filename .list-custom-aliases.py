import sys
from prettytable import PrettyTable
from textwrap import fill

ALIAS_FLAG = "# custom-alias"

def parse_custom_alias(rc_file_line):
    command_category_usage = alias.split("=")
    category_usage = command_category_usage[1].split(ALIAS_FLAG)[1]
    category = category_usage.split("(")[1].split(")")[0].strip()
    usage = category_usage.split(":")[1].strip()
    command = command_category_usage[0].replace("alias ", "")
    return category, command, usage

def render_table(commands_and_usages):
    table = PrettyTable([
        "Command",
        "Usage"
    ])

    for command_and_usage in commands_and_usages:
        table.add_row([
            command_and_usage["command"],
            fill(
                command_and_usage["usage"],
                width=60
            )
        ])
    return table

if __name__ == "__main__":
    """Parses lines containing # custom-alias (category): usage description"""

    aliases = sys.stdin.read()

    parsed_aliases = dict()
    for alias in aliases.strip().split("\n"):
        category, command, usage = parse_custom_alias(alias)
        maybe_commands_and_usages = parsed_aliases.get(category)
        if not maybe_commands_and_usages:
            maybe_commands_and_usages = list()
        maybe_commands_and_usages.append({
            "command": command,
            "usage": usage,
        })
        parsed_aliases[category] = maybe_commands_and_usages 

    aliases_tables = dict()
    for category, commands_and_usages in parsed_aliases.items():
        aliases_tables[category] = render_table(commands_and_usages)

    for category, table in aliases_tables.items():
        print(f"\nAliases related to {category}:\n{table}")
