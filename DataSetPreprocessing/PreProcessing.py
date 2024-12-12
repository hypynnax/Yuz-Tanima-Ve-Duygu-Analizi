import os
import cv2
import shutil
import random


# 1. ADIM (Klasörleri %70 Eğitim ve %30 Test Olarak Ayırma İşlemi)
def split_folders(main_dir, train_dir, test_dir, train_size=378, test_size=162):
    folders = [
        f for f in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, f))
    ]

    # Klasörleri rastgele karıştır
    random.shuffle(folders)

    # Klasörleri train ve test olarak ayır
    train_folders = folders[:train_size]
    test_folders = folders[train_size : train_size + test_size]

    # Train ve test klasörlerini oluştur ve klasörleri taşı
    for folder in train_folders:
        shutil.move(os.path.join(main_dir, folder), os.path.join(train_dir, folder))

    for folder in test_folders:
        shutil.move(os.path.join(main_dir, folder), os.path.join(test_dir, folder))


# Ana klasör ve yeni train/test klasör yolları
main_directory = "DataSet"  # Ana klasör (540 klasörün olduğu yer)
train_directory = "DataSet/train"  # Train için hedef klasör
test_directory = "DataSet/test"  # Test için hedef klasör

# Klasörleri ayır ve taşı
#split_folders(main_directory, train_directory, test_directory)


# 2. ADIM (Sadece Train Klasöründeki Resimlerin Yüzlerini Kırpma İşlemi)
def detect_and_crop_faces(main_dir, cascade_file="haarcascade_frontalface_default.xml"):
    # Haar Cascades classifiar dosyasını yükle
    face_cascade = cv2.CascadeClassifier(cascade_file)

    i = 0
    # Ana klasördeki tüm alt klasörlerde gezin
    for root, dirs, files in os.walk(main_dir):
        i += 1
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                img_path = os.path.join(root, file)

                # Resmi yükle
                img = cv2.imread(img_path)

                # Yüz tespiti için gri tonlamaya çevir
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Yüzleri tespit et
                faces = face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                )

                # Eğer yüz tespit edilirse, yüzü kırp ve kaydet
                if len(faces) > 0:
                    for x, y, w, h in faces:
                        face_img = img[
                            y : y + h, x : x + w
                        ]  # Yüzü orijinal renkli haliyle kırp
                        cv2.imwrite(
                            img_path, face_img
                        )  # Orijinal resmi kırpılmış yüzle değiştir
                else:
                    # Yüz tespit edilemezse orijinal resmi sil
                    os.remove(img_path)

        print(f"{i} / {len(files)}")


# Yüzleri tespit edip kırp
#detect_and_crop_faces(train_directory)


def count_images_in_directory(main_dir):
    total_images = 0
    # Alt klasörleri geziyor
    for root, dirs, files in os.walk(main_dir):
        # Resim dosyalarını sayıyor
        total_images += len(
            [
                file
                for file in files
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
            ]
        )
    return total_images


# Toplam resim sayısını öğren
#total_images = count_images_in_directory("DataSet/test")
#print(f"Toplam resim sayısı: {total_images}")
