from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTChar


def extract_text_and_positions(pdf_path):
    text_positions = []
    for page_layout in extract_pages(pdf_path):
        current_word = ""
        current_position = None

        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            char_text = character.get_text()
                            if char_text.isalnum() or char_text.isspace():
                                if current_position is None:
                                    current_position = {
                                        "x": character.x0,
                                        "y": character.y0,
                                        "width": 0,
                                        "height": character.height,
                                    }
                                current_word += char_text
                                current_position["width"] += character.width
                            else:
                                if current_word.strip():
                                    text_positions.append(
                                        {
                                            "text": current_word.strip(),
                                            "x": current_position["x"],
                                            "y": current_position["y"],
                                            "width": current_position["width"],
                                            "height": current_position["height"],
                                        }
                                    )
                                current_word = ""
                                current_position = None
        # Handle last word if any
        if current_word.strip():
            text_positions.append(
                {
                    "text": current_word.strip(),
                    "x": current_position["x"],
                    "y": current_position["y"],
                    "width": current_position["width"],
                    "height": current_position["height"],
                }
            )

    return text_positions
