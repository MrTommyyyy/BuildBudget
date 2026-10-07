## What changed

- Added `walls` for vertical rectangular perimeters with no floor or roof.
- Corners count once; supports wall thickness, spare blocks and storage calculations.

## Download

Extract the Windows ZIP, open PowerShell in that folder, and run `.\BuildBudget.exe --help`. No separate Python installation required. This is a terminal tool.

Choose `BuildBudget-0.2.0-Windows-x64.zip` for 64-bit Windows or `BuildBudget-0.2.0-Source.zip` for Python 3.11+ on Windows, macOS or Linux. The Windows ZIP includes executable SHA-256 hashes and the MIT licence.

## Validation

Source regression tests and packaged executable behaviour checks run on the Windows build before publishing. The JarCheck desktop interaction still needs manual testing; no claim is made that every desktop configuration has been tested.
