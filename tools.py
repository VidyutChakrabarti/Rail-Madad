from crewai_tools import BaseTool
import cv2
import pytesseract

class OCRTool(BaseTool):
    name: str = "OCR Tool"
    description: str = "Extracts and returns formatted text from an image."
    def _run(self, image_path: str) -> str:
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        extracted_text = pytesseract.image_to_string(image)
        formatted_text = '\n'.join(extracted_text)
        return formatted_text
