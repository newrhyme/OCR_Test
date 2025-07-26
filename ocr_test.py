from paddleocr import PaddleOCR
from PIL import Image, ImageEnhance
from paddleocr import PaddleOCR
import os
import re

ocr = PaddleOCR(use_angle_cls=True, lang='korean')
image_path = 'sample_1.jpeg'  # 이미지 이름

# OCR 수행
result = ocr.predict(image_path)
rec_data = result[0]
texts = rec_data['rec_texts']
scores = rec_data['rec_scores']

# 신뢰도 필터링 + 정규화
clean_texts = [
    re.sub(r'\s+', '', text.lower().replace('㎉', 'kcal').replace('omg', '0mg'))
    for text, score in zip(texts, scores) if score >= 0.6
]

# 라벨 → 수치 추출
labels = ['칼로리', '열량', 'kcal', '탄수화물', '단백질', '지방']
data = {'칼로리': None, '탄수화물': None, '단백질': None, '지방': None}

i = 0
while i < len(clean_texts):
    text = clean_texts[i]

    if any(label in text for label in ['칼로리', '열량', 'kcal']):
        for j in range(i+1, min(i+4, len(clean_texts))):
            match = re.search(r'(\d+(\.\d+)?)\s*(kcal|g|㎉)', clean_texts[j])
            if match and '%' not in clean_texts[j]:
                data['칼로리'] = match.group(0)
                break

    elif '탄수화물' in text:
        for j in range(i+1, min(i+4, len(clean_texts))):
            match = re.search(r'(\d+(\.\d+)?)\s*g', clean_texts[j])
            if match and '%' not in clean_texts[j]:
                data['탄수화물'] = match.group(0)
                break

    elif '단백질' in text:
        for j in range(i+1, min(i+4, len(clean_texts))):
            match = re.search(r'(\d+(\.\d+)?)\s*g', clean_texts[j])
            if match and '%' not in clean_texts[j]:
                data['단백질'] = match.group(0)
                break

    elif '지방' in text:
        for j in range(i+1, min(i+4, len(clean_texts))):
            match = re.search(r'(\d+(\.\d+)?)\s*g', clean_texts[j])
            if match and '%' not in clean_texts[j]:
                data['지방'] = match.group(0)
                break
    i += 1

# 출력
if all(data.values()):
    print("✅ 파싱된 영양성분:", data)
else:
    print("⚠️ 영양성분을 찾을 수 없습니다")

'''
ocr = PaddleOCR(use_angle_cls=True, lang='korean')

image_path = 'sample_1.jpeg'  # 이미지 경로

result = ocr.predict(image_path)

print("📦 전체 OCR 결과:")
rec_data = result[0]

texts = rec_data['rec_texts']
scores = rec_data['rec_scores']
boxes = rec_data['rec_boxes']

for idx, (text, score, box) in enumerate(zip(texts, scores, boxes)):
    print(f"\n🔹 Line {idx + 1}")
    print(f"   🔤 Text: {text}")
    print(f"   📈 Confidence: {score:.3f}")
    print(f"   📦 Bounding Box: {box}")
'''

'''
image = Image.open(image_path)

# (선택) 선명도 높이기, 리사이즈
image = image.convert("L")
image = ImageEnhance.Sharpness(image).enhance(2.0)
if image.width < 300:
    image = image.resize((image.width * 2, image.height * 2))

# 임시 저장
temp_path = "temp_ocr.jpg"
image.save(temp_path)

# OCR 실행
result = ocr.predict(temp_path)

# 결과 출력
print("📦 OCR 결과:")
for line_group in result:
    for line in line_group:
        print(line[1][0])

# 정리
os.remove(temp_path)
'''