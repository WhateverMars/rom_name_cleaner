# rom_name_cleaner

## Description
This is a quick python script which I use to clean up the names of gameboy roms. This will modify the file names of .gb, .gbc and .gba files by removing any bracketed sections and trailing whitespaces to give a more readable name.

eg. Baldur's Gate - Dark Alliance (Europe) (En,Fr,De,Es,It).gba -> Baldur's Gate - Dark Alliance.gba

It will skip all other files and leave them untouched. 

## Usage
1. Download rom_name_cleaner.py
2. Open location of file in Terminal
3. Run "python rom_name_cleaner.py <path_to_rom_folder>"
4. Follow prompts to proceed

### Remember if you are renaming the roms to also rename the save files.