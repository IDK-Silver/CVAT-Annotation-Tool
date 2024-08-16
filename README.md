# CVAT-Annotation-Tool

CVAT-Annotation-Tool是一個專門針對CVAT（Computer Vision Annotation Tool）標註數據進行處理和管理的Python庫。

## 介紹

CVAT-Annotation-Tool提供了一系列功能，用於處理和操作CVAT生成的標註數據。它可以幫助用戶更有效地管理、轉換和導出CVAT標註數據。

## 主要功能

1. 數據加載：從CVAT導出的XML文件中加載標註數據。
2. 標籤管理：添加、修改和合併標籤。
3. 數據轉換：支持將CVAT標註數據轉換為其他常見格式，如YOLO。
4. 數據導出：將處理後的數據導出為各種深度學習框架所需的格式。

## 安裝

要安裝 CVAT-Annotation-Tool，請按照以下步驟操作：

1. 克隆儲存庫：
   ```
   git clone https://github.com/IDK-Silver/CVAT-Annotation-Tool.git
   ```

2. 進入專案目錄：
   ```
   cd CVAT-Annotation-Tool
   ```

3. 使用 pip 安裝套件（以可編輯模式安裝）：
   ```
   pip install -e .
   ```

注意：使用 `-e` 選項進行安裝意味著您可以直接編輯源代碼，這對於開發和測試非常有用。如果您只是想使用這個工具而不打算修改它，您可以省略 `-e` 選項。

## 使用說明

以下是 CVAT-Annotation-Tool 的基本使用說明，包括數據加載、匯出、合併和轉置功能。

### 數據加載

```python
from cvat.core import CVAT

# 創建 CVAT 實例
cvat = CVAT()

# 加載CVAT標註數據
cvat.load('path/to/your/cvat_annotations.xml')

# 獲取元數據
meta = cvat.get_meta()

# 獲取圖像數據
images = cvat.get_images()
```

### 數據匯出

#### YOLO 格式匯出

```python
cvat.export(
    export_path='./export_path',
    export_type='YOLOv1',
    export_args=(
        './data/images/default',
        (0.8, 0.15, 0.05),
        'Kano'
    )
)
```

參數說明：
- `export_path`：指定導出文件的目標路徑。
- `export_type`：指定導出的格式，這裡使用 'YOLOv1' 格式。
- `export_args`：一個元組，包含以下參數：
  1. 圖像路徑：原始圖像文件的位置。
  2. 數據集分割比例：一個包含三個浮點數的元組，分別表示訓練集、驗證集和測試集的比例。在這個例子中，80% 用於訓練，15% 用於驗證，5% 用於測試。
  3. 數據集名稱：為導出的數據集指定一個名稱，這裡使用 'Kano'。

### 圖像分割與遮罩處理

CVAT-Annotation-Tool 提供了強大的圖像分割和遮罩處理功能，使用者可以輕鬆地從 CVAT 標註文件中提取遮罩信息，並進行各種圖像處理操作。

#### 遮罩提取與轉換

```python
# 加載標註文件
file = cvat.core.CVAT()
file.load('./dataset/annotations.xml')

# 獲取圖像和遮罩信息
images_info = file.get_images()
image_info = images_info[0]
image_masks_info = cvat.data.Image.get_masks(image_info)
image_mask_info = image_masks_info[0]

# 轉換 RLE 格式遮罩為二進制遮罩
image_mask = cvat.utility.annotation.rle_to_binary_mask(
    image_mask_info[cvat.data.Mask.Keys.rle],
    image_mask_info[cvat.data.Mask.Keys.height],
    image_mask_info[cvat.data.Mask.Keys.width]
)
```

#### 圖像分割

```python
# 讀取原始圖像
item_image = cv2.imread('./dataset/images/' + image_info[cvat.data.Image.Keys.name])

# 使用遮罩進行圖像分割
segment_image = cvat.utility.image.segment_image_with_mask(
    item_image, image_mask,
    image_mask_info[cvat.data.Mask.Keys.top],
    image_mask_info[cvat.data.Mask.Keys.left],
    is_crop=True
)
```

#### 圖像疊加

```python
# 讀取背景圖像
background_image = cv2.imread('./images/background.jpg')

# 將分割後的圖像疊加到背景上
overlay_image = cvat.utility.image.overlay_image(
    background_image, segment_image,
    (background_image.shape[0] - segment_image.shape[0]) / 2,
    (background_image.shape[1] - segment_image.shape[1]) / 2
)
```

這些功能使得 CVAT-Annotation-Tool 不僅可以處理標註數據，還能進行複雜的圖像處理操作，為計算機視覺項目提供更多可能性。

### 標籤合併

```python
# 假設我們要將 'cat' 標籤合併到 'animal' 標籤中，並添加一個新的屬性 'type'
segment_file.merge_label(object_file.get_meta()[0], '名稱', 'cat', autoconvert=False)
```

參數說明：
- 第一個參數：目標標籤對象（通常是從另一個 CVAT 實例獲取的標籤）
- 第二個參數：新的屬性名稱
- 第三個參數：要合併的源標籤名稱
- `autoconvert`：是否自動轉換標籤類型（默認為 True）

### 數據轉置

```python
# 將指定屬性的值轉換為新的標籤
segment_file.transpose('名稱')
```

參數說明：
- 參數：要轉置的屬性名稱

### 標籤類型轉換

```python
# 將所有標籤轉換為矩形類型
segment_file.convert_label_type(cvat.meta.LabelType.rectangle)
```

參數說明：
- 參數：目標標籤類型（例如 `cvat.meta.LabelType.rectangle`）

## 主要類和方法

- `CVAT`: 主要的類，用於處理CVAT標註數據。
- `Label`: 用於管理標籤的類。
- `Image`: 表示單個圖像及其標註的類。
- `Box`: 表示邊界框的類。
- `Mask`: 表示遮罩的類。

