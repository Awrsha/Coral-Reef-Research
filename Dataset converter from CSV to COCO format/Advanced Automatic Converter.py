import pandas as pd
import json
from pathlib import Path
import hashlib
import datetime
import logging
from typing import Dict, List, Any, Optional
import sys
import os

class COCOConverter:
    def __init__(self, input_path: str, output_path: str, img_width: int = 2704, img_height: int = 1524):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.img_width = img_width
        self.img_height = img_height
        self.setup_logging()
        
    def setup_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('conversion.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
    def validate_input(self, df: pd.DataFrame) -> bool:
        required_columns = ['image', 'label', 'xmin', 'ymin', 'xmax', 'ymax']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logging.error(f"Missing required columns: {missing_columns}")
            return False
            
        if df.empty:
            logging.error("Input CSV file is empty")
            return False
            
        return True
        
    def generate_unique_id(self, text: str) -> int:
        """Generate a deterministic unique ID based on text"""
        return int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
        
    def create_base_structure(self) -> Dict[str, Any]:
        return {
            "info": {
                "description": "Dataset converted from CSV to COCO format",
                "version": "2.0",
                "year": datetime.datetime.now().year,
                "contributor": "Advanced Automatic Converter",
                "date_created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "url": "https://example.com",
                "source": self.input_path.name
            },
            "licenses": [
                {
                    "id": 1,
                    "name": "Attribution-NonCommercial",
                    "url": "https://creativecommons.org/licenses/by-nc/4.0/"
                }
            ],
            "images": [],
            "annotations": [],
            "categories": []
        }
        
    def process_categories(self, df: pd.DataFrame, coco_format: Dict[str, Any]) -> Dict[str, int]:
        unique_labels = sorted(df['label'].unique())
        categories = {}
        
        for label in unique_labels:
            category_id = self.generate_unique_id(label)
            categories[label] = category_id
            
            category_info = {
                "id": category_id,
                "name": label,
                "supercategory": "none",
                "metadata": {
                    "count": int(df[df['label'] == label].shape[0]),
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            
            coco_format["categories"].append(category_info)
            
        return categories
        
    def process_images(self, df: pd.DataFrame, coco_format: Dict[str, Any]) -> Dict[str, int]:
        unique_images = sorted(df['image'].unique())
        image_ids = {}
        
        for img_name in unique_images:
            image_id = self.generate_unique_id(img_name)
            image_ids[img_name] = image_id
            
            image_info = {
                "id": image_id,
                "license": 1,
                "file_name": img_name,
                "height": self.img_height,
                "width": self.img_width,
                "date_captured": datetime.datetime.now().strftime("%Y-%m-%d"),
                "metadata": {
                    "object_count": int(df[df['image'] == img_name].shape[0]),
                    "processed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            
            coco_format["images"].append(image_info)
            
        return image_ids
        
    def process_annotations(self, df: pd.DataFrame, coco_format: Dict[str, Any],
                          image_ids: Dict[str, int], categories: Dict[str, int]) -> None:
        for idx, row in df.iterrows():
            try:
                width = float(row['xmax']) - float(row['xmin'])
                height = float(row['ymax']) - float(row['ymin'])
                
                if width <= 0 or height <= 0:
                    logging.warning(f"Invalid bbox dimensions for annotation {idx + 1}")
                    continue
                    
                bbox = [
                    float(row['xmin']),
                    float(row['ymin']),
                    width,
                    height
                ]
                
                annotation = {
                    "id": self.generate_unique_id(f"{row['image']}_{row['label']}_{idx}"),
                    "image_id": image_ids[row['image']],
                    "category_id": categories[row['label']],
                    "bbox": bbox,
                    "area": float(width * height),
                    "segmentation": [],
                    "iscrowd": 0,
                    "metadata": {
                        "confidence": 1.0,
                        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
                
                coco_format["annotations"].append(annotation)
                
            except (ValueError, KeyError) as e:
                logging.error(f"Error processing annotation {idx + 1}: {str(e)}")
                
    def convert(self) -> Optional[Dict[str, Any]]:
        try:
            logging.info(f"Starting conversion of {self.input_path}")
            df = pd.read_csv(self.input_path)
            
            if not self.validate_input(df):
                return None
                
            coco_format = self.create_base_structure()
            categories = self.process_categories(df, coco_format)
            image_ids = self.process_images(df, coco_format)
            self.process_annotations(df, coco_format, image_ids, categories)
            
            return coco_format
            
        except Exception as e:
            logging.error(f"Conversion failed: {str(e)}")
            return None
            
    def save(self, coco_format: Dict[str, Any]) -> bool:
        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(coco_format, f, ensure_ascii=False, indent=2)
                
            logging.info(f"Successfully saved COCO format to {self.output_path}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save COCO format: {str(e)}")
            return False
            
def main():
    input_file = "FL_Keys_Coral-export.csv"
    output_file = "annotations.json"
    
    converter = COCOConverter(input_file, output_file)
    coco_data = converter.convert()
    
    if coco_data:
        converter.save(coco_data)
        
if __name__ == "__main__":
    main()