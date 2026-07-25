# uts
Proof-of-concept demonstrating the coordinate-integrity flaw in the UTS QR booking path,
based on <https://www.desrever.dev/posts/uts/>. Only `NAME:CODE` is verified by the app, so
the coordinates embedded in a QR are forgeable.

A small Flask backend serves station data (from an embedded SQLite DB) and an AES-ECB encrypt
endpoint; a single-file React frontend lets you pick a station, edit/override the coordinates
(manually or from live GPS), and generate the resulting QR.

## Config

`config.py` holds the AES key:

The actual key employed by the UTS system isn't being shared here due to obvious reasons. One is welcome to 
go through the blog and reproduce the results to extract the key.
