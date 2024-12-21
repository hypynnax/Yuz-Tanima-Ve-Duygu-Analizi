import os
import cv2
import face_recognition
from tqdm import tqdm


# Bulanıklık kontrolü
def is_blurry(image, threshold=100):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var < threshold


# Yüz algılama ve kırpma (face_recognition)
def detect_and_crop_face(image):
    face_locations = face_recognition.face_locations(image)  # Yüzlerin koordinatları
    if len(face_locations) > 0:
        # İlk yüzün koordinatlarını al
        top, right, bottom, left = face_locations[0]
        return image[top:bottom, left:right]  # Yüz kırpılmış hali
    return None  # Yüz bulunamadıysa None döndür


# Klasör işlemleri
def process_folder(input_folder, output_folder, max_images=100, blur_threshold=100):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for person in tqdm(os.listdir(input_folder), desc=f"Processing {input_folder}"):
        person_path = os.path.join(input_folder, person)
        output_person_path = os.path.join(output_folder, person)

        if not os.path.isdir(person_path):
            continue

        if not os.path.exists(output_person_path):
            os.makedirs(output_person_path)

        images = []
        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            try:
                image = cv2.imread(img_path)
                if image is None:
                    continue  # Açılmayan dosyaları atla

                if is_blurry(image, threshold=blur_threshold):
                    continue  # Bulanık dosyaları atla

                cropped_face = detect_and_crop_face(image)
                if cropped_face is not None:
                    images.append((img_name, cropped_face))

            except Exception as e:
                print(f"Error processing {img_path}: {e}")

        # En kaliteli max_images kadar resmi seç ve kaydet
        images = images[:max_images]  # Daha fazla resim varsa sınırlıyoruz
        for img_name, face in images:
            output_path = os.path.join(output_person_path, img_name)
            cv2.imwrite(output_path, face)


# Train ve test klasörlerini işle
train_input_folder = "DataSet\\train"
test_input_folder = "DataSet\\test"
train_output_folder = "PreDataSet\\processed_train"
test_output_folder = "PreDataSet\\processed_test"

process_folder(
    train_input_folder, train_output_folder, max_images=100, blur_threshold=100
)
process_folder(
    test_input_folder, test_output_folder, max_images=100, blur_threshold=100
)

print("Processing complete!")
