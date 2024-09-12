import argparse
import logging
from pathlib import Path
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Clean and rename ROM files in a specified folder."
    )
    parser.add_argument(
        "folder_path", type=str, help="Path to the folder containing ROM files."
    )
    return parser.parse_args()


def confirm_folder_path(folder_path):
    """Confirm if the folder path exists and ask user for confirmation to proceed."""
    try:
        if not folder_path.exists():
            logging.error("Folder does not exist.")
            return False
    except Exception as e:
        logging.error(f"Error checking folder path: {e}")
        return False

    logging.info(f"Folder path: {folder_path}")
    confirm = input("Proceed with cleaning the files? (y/n): ")
    return confirm.lower() == "y"


def filter_by_supported_extensions(file_paths):
    """Filter file paths by listed extensions."""
    supported_rom_types = {
        ".gb",  # Game Boy
        ".gbc",  # Game Boy Color
        ".gba",  # Game Boy Advance
        ".nes",  # NES
        ".nez",  # NES
        ".sfc",  # SNES
        ".gen",  # Sega Genesis
        ".n64",  # Nintendo 64
        ".gcm",  # GameCube
        ".gcz",  # GameCube
        ".nds",  # Nintendo DS
        ".3ds",  # Nintendo 3DS
        ".nsp",  # Nintendo Switch
        ".vpk",  # PS Vita
        ".sav",  # Save file ext
    }
    return [
        file_path for file_path in file_paths if file_path.suffix in supported_rom_types
    ]


def clean_file_name(file_path):
    """Clean the file name by removing content inside brackets and trailing spaces or dots."""
    file_stem = file_path.stem
    file_ext = file_path.suffix

    file_stem = re.sub(r"\(.*?\)", "", file_stem)
    file_stem = re.sub(
        r"\s+", " ", file_stem
    )  # Replace multiple spaces with a single space
    file_stem = file_stem.strip().rstrip(".")

    return file_stem + file_ext


def rename_file_success(folder_path, old_file_name, new_file_name):
    """Rename the file from old_file_name to new_file_name in the specified folder."""
    old_file_path = folder_path / old_file_name
    new_file_path = folder_path / new_file_name

    if new_file_path.exists():
        logging.error(f"File {new_file_name} already exists. Leaving {old_file_name} unchanged.")
        return False
    else:
        old_file_path.rename(new_file_path)
        return True


def rom_name_cleaner(folder_path):
    """Clean and rename ROM files in the given folder."""

    file_paths = sorted(folder_path.iterdir(), key=lambda x: x.name)

    file_paths = filter_by_supported_extensions(file_paths)

    # Count the number of files renamed or skipped
    num_renamed_files = 0

    # Clean file names one by one
    for file_path in file_paths:

        cleaned_file_name = clean_file_name(file_path)
        file_name = file_path.name

        if file_name != cleaned_file_name:

            try:
                if rename_file_success(folder_path, file_name, cleaned_file_name):
                    num_renamed_files += 1
            except Exception as e:
                logging.error(f"Error renaming {file_name}: {e}")

    if num_renamed_files == 0:
        logging.info("No files renamed.")
    else:
        logging.info(f"Renamed {num_renamed_files} files.")


def main():
    args = parse_arguments()
    folder_path = Path(args.folder_path)

    if confirm_folder_path(folder_path):
        rom_name_cleaner(folder_path)


if __name__ == "__main__":
    main()
