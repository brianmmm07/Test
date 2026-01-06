"""Module to extract figures and images from arXiv papers."""
import fitz  # PyMuPDF
import requests
import os
from typing import List, Dict, Optional
from PIL import Image
import io

class FigureExtractor:
    """Extract figures and images from arXiv PDF papers."""

    def __init__(self, output_dir: str = "paper_figures"):
        """
        Initialize figure extractor.

        Args:
            output_dir: Directory to save extracted figures
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def download_pdf(self, pdf_url: str, paper_id: str) -> Optional[str]:
        """
        Download PDF from arXiv.

        Args:
            pdf_url: URL to the PDF
            paper_id: arXiv paper ID

        Returns:
            Path to downloaded PDF, or None if failed
        """
        try:
            # Sanitize paper ID for filename
            safe_id = paper_id.replace('http://arxiv.org/abs/', '').replace('/', '_')
            pdf_path = os.path.join(self.output_dir, f"{safe_id}.pdf")

            # Check if already downloaded
            if os.path.exists(pdf_path):
                return pdf_path

            # Download PDF
            print(f"    Downloading PDF from {pdf_url}...")
            response = requests.get(pdf_url, timeout=30)
            response.raise_for_status()

            # Save PDF
            with open(pdf_path, 'wb') as f:
                f.write(response.content)

            return pdf_path

        except Exception as e:
            print(f"    Error downloading PDF: {e}")
            return None

    def extract_figures(self, pdf_path: str, paper_id: str, max_figures: int = 3) -> List[str]:
        """
        Extract figures from PDF.

        Args:
            pdf_path: Path to PDF file
            paper_id: arXiv paper ID
            max_figures: Maximum number of figures to extract

        Returns:
            List of paths to extracted figure images
        """
        try:
            figure_paths = []
            safe_id = paper_id.replace('http://arxiv.org/abs/', '').replace('/', '_')

            # Open PDF
            doc = fitz.open(pdf_path)

            # Extract images from first few pages (where overview figures usually are)
            pages_to_check = min(5, len(doc))  # Check first 5 pages
            images_found = []

            for page_num in range(pages_to_check):
                page = doc[page_num]
                image_list = page.get_images()

                for img_index, img in enumerate(image_list):
                    try:
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]

                        # Filter by size (likely to be figures, not icons)
                        if len(image_bytes) > 10000:  # > 10KB
                            # Open image to check dimensions
                            pil_image = Image.open(io.BytesIO(image_bytes))
                            width, height = pil_image.size

                            # Filter by dimensions (real figures are usually larger)
                            if width > 200 and height > 200:
                                images_found.append({
                                    'bytes': image_bytes,
                                    'ext': image_ext,
                                    'page': page_num,
                                    'size': len(image_bytes),
                                    'width': width,
                                    'height': height
                                })

                    except Exception as e:
                        continue

            # Sort by page number (prefer early figures) and size
            images_found.sort(key=lambda x: (x['page'], -x['size']))

            # Save top figures
            for i, img_data in enumerate(images_found[:max_figures]):
                figure_path = os.path.join(
                    self.output_dir,
                    f"{safe_id}_fig_{i+1}.{img_data['ext']}"
                )

                with open(figure_path, "wb") as f:
                    f.write(img_data['bytes'])

                figure_paths.append(figure_path)
                print(f"    Extracted figure {i+1}: {img_data['width']}x{img_data['height']} from page {img_data['page']+1}")

            doc.close()
            return figure_paths

        except Exception as e:
            print(f"    Error extracting figures: {e}")
            return []

    def get_paper_figures(self, paper: Dict, max_figures: int = 3) -> List[str]:
        """
        Get figures for a paper (download PDF and extract).

        Args:
            paper: Paper dictionary with pdf_url and id
            max_figures: Maximum number of figures to extract

        Returns:
            List of paths to extracted figures
        """
        print("    Extracting figures from PDF...")

        # Download PDF
        pdf_path = self.download_pdf(paper['pdf_url'], paper['id'])
        if not pdf_path:
            return []

        # Extract figures
        figure_paths = self.extract_figures(pdf_path, paper['id'], max_figures)

        return figure_paths

    def cleanup_old_pdfs(self, keep_days: int = 7):
        """
        Clean up old downloaded PDFs.

        Args:
            keep_days: Number of days to keep PDFs
        """
        import time

        try:
            now = time.time()
            for filename in os.listdir(self.output_dir):
                filepath = os.path.join(self.output_dir, filename)
                if os.path.isfile(filepath):
                    # Check file age
                    file_age_days = (now - os.path.getmtime(filepath)) / 86400
                    if file_age_days > keep_days and filename.endswith('.pdf'):
                        os.remove(filepath)
                        print(f"Cleaned up old PDF: {filename}")

        except Exception as e:
            print(f"Error cleaning up PDFs: {e}")
