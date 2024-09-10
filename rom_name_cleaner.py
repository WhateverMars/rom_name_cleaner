import argparse
import logging
from pathlib import Path

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


def filter_by_gameboy_extension(file_paths):
    """Filter file paths by Gameboy extensions."""
    return [
        file_path
        for file_path in file_paths
        if file_path.suffix in {".gb", ".gbc", ".gba"}
    ]


def clean_file_name(file_path):
    """Clean the file name by removing content inside brackets and trailing spaces or dots."""
    file_stem = file_path.stem
    file_ext = file_path.suffix

    bracket_index = file_stem.find("(")
    if bracket_index != -1:
        file_stem = file_stem[:bracket_index]

    file_stem = file_stem.strip().rstrip(".")

    return file_stem + file_ext


def rename_file(folder_path, old_file_name, new_file_name):
    """Rename the file from old_file_name to new_file_name in the specified folder."""
    old_file_path = folder_path / old_file_name
    new_file_path = folder_path / new_file_name
    old_file_path.rename(new_file_path)


def rom_name_cleaner(folder_path):
    """Clean and rename ROM files in the given folder."""

    file_paths = list(folder_path.iterdir())

    # Filter the file names that end in .gb, .gbc, .gba
    file_paths = filter_by_gameboy_extension(file_paths)

    # Count the number of files renamed or skipped
    num_renamed_files = 0

    # Clean file names
    for file_path in file_paths:

        cleaned_file_name = clean_file_name(file_path)
        file_name = file_path.name

        if file_name != cleaned_file_name:

            try:
                rename_file(folder_path, file_name, cleaned_file_name)
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
