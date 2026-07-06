import tempfile
import unittest
from pathlib import Path

from rom_name_cleaner import (
    clean_file_name,
    filter_by_supported_extensions,
    rename_file_success,
    rom_name_cleaner,
)


class CleanFileNameTests(unittest.TestCase):
    def assert_cleans_to(self, original, expected):
        self.assertEqual(clean_file_name(Path(original)), expected)

    def test_strips_region_tag(self):
        self.assert_cleans_to("Game Name (USA).gba", "Game Name.gba")

    def test_strips_multiple_tags(self):
        self.assert_cleans_to("Game Name (USA) (Rev 1).gba", "Game Name.gba")

    def test_collapses_double_spaces(self):
        self.assert_cleans_to("Game  Name (Europe).gba", "Game Name.gba")

    def test_leaves_clean_names_unchanged(self):
        self.assert_cleans_to("Game Name.gb", "Game Name.gb")

    def test_unknown_extension(self):
        self.assert_cleans_to("Unknown File (ver 1).xyz", "Unknown File.xyz")

    def test_strips_trailing_spaces(self):
        self.assert_cleans_to("Game Name (USA)   .gba", "Game Name.gba")

    def test_square_brackets(self):
        self.assert_cleans_to("Game Name [USA].gba", "Game Name.gba")

    def test_strips_trailing_dots(self):
        self.assert_cleans_to("Game Name (USA)...gba", "Game Name.gba")

    def test_strips_mixed_trailing_dots_and_spaces(self):
        self.assert_cleans_to("Game Name (USA) . ..gba", "Game Name.gba")

    def test_preserves_internal_dots(self):
        self.assert_cleans_to("Dr. Mario (USA).gb", "Dr. Mario.gb")


class FilterExtensionsTests(unittest.TestCase):
    def test_keeps_only_supported_extensions(self):
        paths = [Path("a.gba"), Path("b.txt"), Path("c.sav"), Path("d.iso")]
        self.assertEqual(
            filter_by_supported_extensions(paths),
            [Path("a.gba"), Path("c.sav")],
        )

    def test_empty_list(self):
        self.assertEqual(filter_by_supported_extensions([]), [])

    def test_all_unsupported(self):
        paths = [Path("a.txt"), Path("b.doc"), Path("c.pdf")]
        self.assertEqual(filter_by_supported_extensions(paths), [])


class FileSystemTestCase(unittest.TestCase):
    """Base class: fresh temp folder per test, plus file helpers."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.folder = Path(self._tmp.name)

    def make_files(self, *names):
        for name in names:
            (self.folder / name).touch()

    def folder_contents(self):
        return sorted(p.name for p in self.folder.iterdir())


class RenameFileTests(FileSystemTestCase):
    def test_renames_file(self):
        self.make_files("Game (USA).gba")

        result = rename_file_success(self.folder, "Game (USA).gba", "Game.gba")

        self.assertTrue(result)
        self.assertEqual(self.folder_contents(), ["Game.gba"])

    def test_skips_when_target_exists(self):
        self.make_files("Game (USA).gba", "Game.gba")

        result = rename_file_success(self.folder, "Game (USA).gba", "Game.gba")

        self.assertFalse(result)
        self.assertIn("Game (USA).gba", self.folder_contents())

    def test_rename_dry_run(self):
        self.make_files("Game (USA).gba")

        result = rename_file_success(
            self.folder, "Game (USA).gba", "Game.gba", dry_run=True
        )

        self.assertTrue(result)
        self.assertEqual(self.folder_contents(), ["Game (USA).gba"])

    def test_rename_dry_run_target_exists(self):
        self.make_files("Game (USA).gba", "Game.gba")

        result = rename_file_success(
            self.folder, "Game (USA).gba", "Game.gba", dry_run=True
        )

        self.assertFalse(result)
        self.assertIn("Game (USA).gba", self.folder_contents())
        self.assertIn("Game.gba", self.folder_contents())


class RomNameCleanerTests(FileSystemTestCase):
    def test_dry_run_touches_nothing(self):
        self.make_files("Game (USA).gba")
        before = self.folder_contents()

        rom_name_cleaner(self.folder, dry_run=True)

        self.assertEqual(self.folder_contents(), before)

    def test_when_collision_no_update(self):
        self.make_files("Game (USA).gba", "Game (EU).gba")

        rom_name_cleaner(self.folder, dry_run=False)

        self.assertEqual(self.folder_contents(), ["Game (EU).gba", "Game (USA).gba"])


if __name__ == "__main__":
    unittest.main()
