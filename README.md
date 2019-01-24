# Telegram Bot that receives a pic and print it using a FENIX IMVICO VL42 (Epson TK41)

This project prints a ticket for the event "Quiero ser ingeniera", organized by University of Granada.

Telegram Bot works with pyTelegramBotAPI

Thermal printer FENIX IMVICO VL42 (Epson TK41) works with the [library developed by Pablo Garrido, ThermalLibrary](https://github.com/pablogs9/ThermalLibrary), with some modifications.

# Thermal ESC/POS Ticket Printing Library

The Thermal Library implements lots of commands according to the ESC/POS standard:

- Start the serial connection with the printer
- Format text: emphasis, underline, align, character size, text rotation, inverted colors (white text and black background).
- Change between small or standard font size
- Resize and print bitmaps given as a arbitrary image format (JPEG,PNG...)

Here you can find two sample programs which use the Thermal Library:
- A preview generator: preview.py
- A sample printing program: ThermalPhoto.py

Some samples:

![In](https://raw.githubusercontent.com/pablogs9/ThermalLibary/master/in.jpg)

![Out](https://raw.githubusercontent.com/pablogs9/ThermalLibary/master/out.jpg)
