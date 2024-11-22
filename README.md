# 🌊 Advanced Coral Reef Analysis with SAM2 & COCO Tools
> An integrated suite for coral reef research combining Meta AI's SAM2 and automated annotation tools

## 🔍 System Architecture
```mermaid
graph TD
    A[Input Images] -->|SAM2 Pipeline| B[Image Processing]
    B --> C[Instance Segmentation]
    C --> D[Mask Generation]
    D -->|Format Conversion| E[CSV Format]
    D -->|Direct Export| F[COCO Format]
    E -->|Converter| F
    F --> G[Final Dataset]

    subgraph "Processing Pipeline"
    B
    C
    D
    end

    subgraph "Data Format Handling"
    E
    F
    end
```

## 🚀 Key Features

```mermaid
mindmap
  root((Coral Analysis Suite))
    SAM2 Integration
      Advanced instance segmentation
      Interactive prompting
      Automated mask generation
    Format Conversion
      CSV to COCO converter
      Automatic ID generation
      Metadata enrichment
    Quality Control
      Error handling
      Validation checks
      Progress tracking
    Export Capabilities
      COCO JSON format
      CSV annotations
      Visualization tools
```

## ⚙️ Components

1. **SAM2 Segmentation Engine**   - Instance segmentation
   - Multi-mask output
   - GPU optimization
   - Interactive prompting

2. **Format Converter**
   - CSV to COCO transformation
   - Deterministic ID generation
   - Comprehensive error handling
   - Progress tracking

3. **Visualization Tools**
   - Mask visualization
   - Bounding box display
   - Annotation overlay
   - Quality metrics

## 🛠️ Installation

```bash
# Clone repository
git clone https://github.com/Awrsha/Coral-Reef-Research.git
cd Coral-Reef-Research

# Install dependencies
pip install -r requirements.txt

# Download SAM2 model
wget https://dl.fbaipublicfiles.com/segment_anything_2/072824/sam2_hiera_large.pt -P checkpoints/
```

## 📊 Data Flow
```mermaid
sequenceDiagram
    participant User
    participant SAM2
    participant Converter
    participant Storage

    User->>SAM2: Input Image
    SAM2->>SAM2: Generate Masks
    SAM2->>Converter: Segmentation Data
    Converter->>Converter: Format Processing
    Converter->>Storage: COCO JSON
    Storage->>User: Final Dataset
```

## 💻 Usage Examples

### SAM2 Segmentation
```python
from sam2_coral_segmentation import setup_sam2, process_image

# Initialize model
model, device = setup_sam2()

# Process image
masks, scores = process_image("coral_image.jpg", model)
```

### Format Conversion
```python
from coco_converter import COCOConverter

converter = COCOConverter(
    input_path="annotations.csv",
    output_path="coco_dataset.json",
    img_width=2704,
    img_height=1524
)

coco_data = converter.convert()
converter.save(coco_data)
```

## 📊 Output Formats

### COCO JSON Structure

```json
{
    "info": {"description": "Coral Reef Dataset"},
    "images": [
        {
            "id": 1,
            "width": 2704,
            "height": 1524,
            "file_name": "coral_001.jpg"
        }
    ],
    "annotations": [...],
    "categories": [...]
}
```

## Developers 👨🏻‍💻

<div align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/m-kashani">
          <img src="https://avatars.githubusercontent.com/u/3967516?v=4" width="100px;" style="border-radius:50%;" alt="Mahdi Kashani"/>
          <br />
          <sub><b>Mahdi Kashani</b></sub>
        </a>
        <br />
        <a href="https://www.linkedin.com/in/m-kashani/">
          <img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=flat&logo=Linkedin&logoColor=white" />
        </a>
      </td>
      <br />
      <td align="center">
        <a href="https://github.com/Awrsha">
          <img src="https://avatars.githubusercontent.com/u/89135083?v=4" width="100px;" style="border-radius:50%;" alt="Amir M. Parvizi"/>
          <br />
          <sub><b>Amir M. Parvizi</b></sub>
        </a>
        <br />
        <a href="https://www.linkedin.com/in/awrsha/">
          <img src="https://img.shields.io/badge/-LinkedIn-0077B5?style=flat&logo=Linkedin&logoColor=white" />
        </a>
      </td>
    </tr>
  </table>
</div>

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
