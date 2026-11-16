# Hex-ID-App

Point your phone camera at any colour, line it up in the crosshair, and get its HEX, RGB, HSL and CMYK codes.

**Live app:** https://cmidzleton.github.io/Hex-ID-App/ (on iPhone: open in Safari, then Share → Add to Home Screen)

## Features
- Live camera with centre crosshair; each capture averages several frames
- Photo mode with pinch-zoom, pan and a pixel magnifier
- White-paper calibration for the room's light
- Patch size (small / medium / large), quality meter for glare, dim light and uneven patches
- Nearest CSS colour name, WCAG contrast against white and black
- Accuracy check against a known HEX
- Works offline once installed

Readings are approximate: phone cameras adjust exposure and white balance on their own.

## Editing
The app source is `src/app.html`. The app name is set once in `src/build.py` (`APP_NAME`).
After any change, run `python3 src/build.py` (needs Pillow for icons) and commit the regenerated files in the repo root.
