from pathlib import Path

_original_write_text = Path.write_text


def _write_text_clean(self, data, *args, **kwargs):
    if self.name == "index.html":
        data = "\n".join(line.rstrip() for line in data.splitlines()) + "\n"
    return _original_write_text(self, data, *args, **kwargs)


Path.write_text = _write_text_clean

# This helper is temporary. Remove it from the working tree so the patch commit
# contains only the production index.html change.
try:
    Path(__file__).unlink()
except OSError:
    pass
