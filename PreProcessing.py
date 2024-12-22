import os
import cv2
import face_recognition
import shutil
import random
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
def process_folder(input_folder, output_folder, blur_threshold=100):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for person in tqdm(os.listdir(input_folder), desc=f"Processing {input_folder}"):
        person_path = os.path.join(input_folder, person)
        output_person_path = os.path.join(output_folder, person)

        if not os.path.isdir(person_path):
            continue

        if not os.path.exists(output_person_path):
            os.makedirs(output_person_path)

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
                    output_path = os.path.join(output_person_path, img_name)
                    cv2.imwrite(output_path, cropped_face)

            except Exception as e:
                print(f"Error processing {img_path}: {e}")


# Test setini oluşturma (yüzde 30 resim taşıma işlemi)
def split_test_set(source_dir, test_dir, percentage=30):
    os.makedirs(test_dir, exist_ok=True)

    for class_name in os.listdir(source_dir):
        class_path = os.path.join(source_dir, class_name)
        if os.path.isdir(class_path):  # Eğer bu bir klasörse (sınıf)
            images = os.listdir(class_path)
            if len(images) > 0:  # Klasörde en az bir resim varsa
                num_test_images = max(
                    1, int(len(images) * percentage / 100)
                )  # Yüzde 30 resim seç
                test_images = random.sample(
                    images, num_test_images
                )  # Rastgele yüzde 30 resmi seç

                # Test klasöründeki alt klasörü oluştur
                test_class_dir = os.path.join(test_dir, class_name)
                os.makedirs(test_class_dir, exist_ok=True)

                # Seçilen resimleri test klasörüne taşı
                for img in test_images:
                    src_path = os.path.join(class_path, img)
                    dst_path = os.path.join(test_class_dir, img)
                    shutil.move(src_path, dst_path)  # Taşıma işlemi


# Ana işlemler
train_input_folder = "DataSet\\train"
train_output_folder = "PreDataSet\\train"
test_output_folder = "PreDataSet\\test"

# 1. Yüzleri kırp ve ön işle
process_folder(train_input_folder, train_output_folder, blur_threshold=100)

# 2. Test setini ayır (yüzde 30)
split_test_set(train_output_folder, test_output_folder, percentage=30)

print("Tüm işlemler başarıyla tamamlandı!")
