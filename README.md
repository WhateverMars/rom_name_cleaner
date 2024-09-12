# rom_name_cleaner

## Description
This is a quick python script which I use to clean up the names of gameboy roms. This will modify the file names of rom files from the below list by removing any bracketed sections and trailing whitespaces to give a more readable name. If the new name would clash with and existing file it will leave it unchanged. This should allow for translated version to remain alongside originals.

eg. Baldur's Gate - Dark Alliance (Europe) (En,Fr,De,Es,It).gba -> Baldur's Gate - Dark Alliance.gba

It will skip all other files and leave them untouched. 

## Supported roms
 - ".gb",  # Game Boy
 - ".gbc",  # Game Boy Color
 - ".gba",  # Game Boy Advance
 - ".nes",  # NES
 - ".nez",  # NES
 - ".sfc",  # SNES
 - ".gen",  # Sega Genesis
 - ".n64",  # Nintendo 64
 - ".gcm",  # GameCube
 - ".gcz",  # GameCube
 - ".nds",  # Nintendo DS
 - ".3ds",  # Nintendo 3DS
 - ".nsp",  # Nintendo Switch
 - ".vpk",  # PS Vita
 - ".sav",  # Save file ext
## Usage
1. Download rom_name_cleaner.py
2. Open location of file in Terminal
3. Run "python rom_name_cleaner.py <path_to_rom_folder>"
4. Follow prompts to proceed

### Remember if you are renaming the roms to also rename the save files.
This can be done by running the file again on any save folders containing .sav files.