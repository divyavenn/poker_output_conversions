import re
from datetime import datetime
from pathlib import Path

def convert_to_acr_format(input_text: str) -> str:
    """
    Convert raw hand history text (Poker Hand #ring_…) into ACR-style format,
    renaming "Dealt to Hero" to "Hero [cards]".
    """
    hands = input_text.strip().split('\n\n')
    acr_hands = []

    for hand in hands:
        lines = hand.strip().split('\n')
        if not lines or not lines[0].startswith("Poker Hand"):
            continue

        # Parse header, e.g.: 
        #   Poker Hand #ring_880304354: NLH No Limit ($0.1/$0.2) - 2025/05/16 10:22:57
        header_match = re.match(
            r"Poker Hand #(\S+): (.+) \(\$(\d+(?:\.\d+)?)/\$(\d+(?:\.\d+)?)\) - (.+)",
            lines[0]
        )
        if not header_match:
            continue

        hand_id, game_type, sb, bb, timestamp = header_match.groups()

        # Parse table line, e.g.:
        #   Table 'SB+BOMB: 8-20' 5-max Seat #3 is the button
        table_line = lines[1]
        table_match = re.match(
            r"Table '(.*?)' (\d+)-max Seat #(\d+) is the button", 
            table_line
        )
        if not table_match:
            continue

        table_name, max_players, button_seat = table_match.groups()

        # Reformat timestamp → add "UTC"
        try:
            dt = datetime.strptime(timestamp.strip(), "%Y/%m/%d %H:%M:%S")
            timestamp_formatted = dt.strftime("%Y/%m/%d %H:%M:%S UTC")
        except ValueError:
            timestamp_formatted = timestamp.strip() + " UTC"

        # Build ACR-style header lines:
        acr_lines = [
            f"Hand #{hand_id} - {game_type} - ${sb}/{bb} - {timestamp_formatted}",
            f"{table_name} {max_players}-max Seat #{button_seat} is the button"
        ]

        # Rename “Dealt to Hero [xx xx]” → “Hero [xx xx]” and copy all other lines
        for line in lines[2:]:
            hero_line = re.sub(r"^Dealt to Hero\s", "Hero ", line)
            acr_lines.append(hero_line)

        acr_hands.append("\n".join(acr_lines))

    return "\n\n".join(acr_hands)
  
if __name__ == "__main__":
    from tkinter import Tk, filedialog
    import traceback
    from datetime import datetime

    # Hide the main tkinter window
    Tk().withdraw()

    # Open a file dialog to select the raw folder
    raw_folder = Path(filedialog.askdirectory(title="Select Raw Hands Directory"))
    converted_folder = Path(raw_folder / "converted_hands")
    converted_folder.mkdir(exist_ok=True)

    # Create or append to error log file
    error_log = converted_folder / "error_log.txt"
    errors_occurred = False

    for txt_file in sorted(raw_folder.glob("*.txt")):
        try:
            raw_text = txt_file.read_text(encoding='utf-8', errors='ignore')
            converted_text = convert_to_acr_format(raw_text)

            out_name = f"{txt_file.stem}_converted.txt"
            out_path = converted_folder / out_name
            out_path.write_text(converted_text, encoding='utf-8')
        except Exception as e:
            errors_occurred = True
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_message = f"\n[{timestamp}] Error converting {txt_file.name}:\n{str(e)}\n{traceback.format_exc()}\n"
            with open(error_log, 'a', encoding='utf-8') as f:
                f.write(error_message)

    if errors_occurred:
        print(f"Done with errors. Check {error_log} for details.")
    else:
        print("Done. All files converted successfully.")
    print(f"Converted files are in {converted_folder}/")
