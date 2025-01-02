import traceback
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from firebase_admin import db
from .models import *
from deepface import DeepFace
import base64
import cv2
import cv2.data
import numpy as np
from datetime import datetime
from PIL import Image
from io import BytesIO
from mtcnn import MTCNN
from datetime import datetime
import json


usersDictionary = {}
usersFaceDictionary = {}
analyzed_face_id = ""
detector = MTCNN()


# Veritabanındaki Tüm Verileri Alma Methodu
def getDatabase():
    ref = db.reference("users")
    users = ref.get()
    if users:
        for user_id, user_data in users.items():
            usersDictionary.setdefault(user_id, user_data)
        ref = db.reference("usersFace")
        usersFace = ref.get()
        if usersFace:
            for user_data in usersFace.values():
                usersFaceDictionary.setdefault(user_data["photo"], user_data["userId"])


def processing(request):
    getDatabase()
    return render(request, "../templates/FaceRecoApp/FaceReco.html")


# Veritabanında Gelen Resimdeki Kişiyi Arama Methodu
def searchFace(face_vector, emotion):
    global analyzed_face_id
    for key, value in usersFaceDictionary.items():
        distance = np.linalg.norm(np.array(face_vector) - np.array(json.loads(key)))
        print("uzaklık : ", distance)
        if distance < 1.0:
            user = usersDictionary[value]
            if analyzed_face_id != value and emotion != "":
                if registerEmotion(value, user, emotion):
                    analyzed_face_id = value

            return user


# Veritabanına Tespit Edilen Duygu Verilerini Kayıt Etme Methodu
def registerEmotion(value, user, emotion):
    try:
        ref = db.reference("analysis")
        ref.push(
            {
                "id": value,
                "name": user["name"],
                "surname": user["surname"],
                "job": user["job"],
                "old": datetime.now().year
                - datetime.strptime(user["date_of_birth"], "%d/%m/%Y").year,
                "gender": "ERKEK" if user["gender"] else "KADIN",
                "dateDetected": datetime.now().strftime("%H:%M:%S - %d/%m/%Y"),
                "detectedEmotion": emotion,
            }
        )

        return True
    except Exception as e:
        print(e)
        return False


# Yüz Tanıma Methodu
@csrf_exempt
@require_POST
def reco(request):
    name = "--"
    surname = "--"
    dateOfBirth = "--/--/----"
    bloodGroup = "--"
    job = "--"
    size = "--"
    weight = "--"
    age = "--"
    gender = "--"
    emotion = "--"

    try:
        if request.method == "POST":
            photo = request.POST.get("file")
            format, imgstr = photo.split(";base64,")
            img_data = base64.b64decode(imgstr)
            image = Image.open(BytesIO(img_data))
            image_np = np.array(image)
            img_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

            faces = detector.detect_faces(img_rgb)

            for face in faces:
                x, y, width, height = face["box"]
                keypoints = face["keypoints"]
                face_image = img_rgb[y : y + height, x : x + width]
                face_vector = DeepFace.represent(face_image, model_name="VGG-Face")
                dominant_emotion = ""
                try:
                    analysis = DeepFace.analyze(img_path=img_rgb, actions=["emotion"])

                    dominant_emotion = (
                        analysis[0]["dominant_emotion"]
                        if isinstance(analysis, list)
                        else analysis["dominant_emotion"]
                    )
                except Exception as e:
                    print(f"Bir hata oluştu: {e}")

                findFace = searchFace(face_vector[0]['embedding'], dominant_emotion)
                if findFace:
                    name = findFace["name"]
                    surname = findFace["surname"]
                    dateOfBirth = findFace["date_of_birth"]
                    bloodGroup = findFace["blood_group"]
                    job = findFace["job"]
                    size = findFace["size"]
                    weight = findFace["weight"]
                    birth_date = datetime.strptime(
                        findFace["date_of_birth"], "%d/%m/%Y"
                    )
                    current_date = datetime.now()
                    age = (
                        current_date.year
                        - birth_date.year
                        - (
                            (current_date.month, current_date.day)
                            < (birth_date.month, birth_date.day)
                        )
                    )
                    gender = findFace["gender"]
                    emotion = dominant_emotion
                    break
    except Exception as e:
        print(e)
        traceback.print_exc()

    return JsonResponse(
        {
            "name": name,
            "surname": surname,
            "dateOfBirth": dateOfBirth,
            "bloodGroup": bloodGroup,
            "job": job,
            "size": size,
            "weight": weight,
            "age": age,
            "gender": gender,
            "emotion": emotion,
        }
    )


# Veritabanına Gelen Verileri Kayıt Etme Methodu
def registerDatabase(user):
    ref = db.reference("users")
    userResponse = ref.push(user.to_dict())
    usersDictionary.setdefault(userResponse.key, user)

    return userResponse.key


# Veritabanına Gelen Resmi Kayıt Etme Methodu
def registerImage(userPhoto):
    ref = db.reference("usersFace")
    usersFace = ref.push(userPhoto.to_dict())
    usersFaceDictionary.setdefault(usersFace.key, userPhoto)


# Veritabanından Gelen İd Verisini Silme Methodu
def deleteDatabase(id):
    ref = db.reference(f"users/{id}")
    ref.delete()
    if id in usersDictionary:
        del usersDictionary[id]


# Veritabanından Gelen İd'nin Resmini Silme Methodu
def deleteImage(id):
    keys_to_delete = [
        key for key, value in usersFaceDictionary.items() if value.userId == id
    ]
    for key in keys_to_delete:
        ref = db.reference(f"usersFace/{key}")
        ref.delete()
        del usersFaceDictionary[key]


# Yüz Kayıt Methodu
@csrf_exempt
@require_POST
def rec(request):
    id = ""
    try:
        if request.method == "POST":
            photos = [
                request.POST.get("photoOne"),
                request.POST.get("photoTwo"),
                request.POST.get("photoThree"),
            ]
            user = User(
                name=request.POST.get("name"),
                surname=request.POST.get("surname"),
                date_of_birth=request.POST.get("date_of_birth"),
                job=request.POST.get("job"),
                size=request.POST.get("size"),
                weight=request.POST.get("weight"),
                blood_group=request.POST.get("blood_group"),
                gender=request.POST.get("gender"),
            )

            id = registerDatabase(user)

            for photo in photos:
                format, imgstr = photo.split(";base64,")
                img_data = base64.b64decode(imgstr)
                image = Image.open(BytesIO(img_data))
                image_np = np.array(image)
                img_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

                faces = detector.detect_faces(img_rgb)
                for face in faces:
                    x, y, width, height = face["box"]
                    keypoints = face["keypoints"]

                    face_image = img_rgb[y : y + height, x : x + width]
                    face_vector = json.dumps(DeepFace.represent(face_image, model_name="VGG-Face")[0]['embedding'])

                    userPhoto = UserPhoto(
                        userId=id,
                        photo=face_vector,
                    )
                    registerImage(userPhoto)
                    break

            status = True
            message = "YÜZ KAYIT İŞLEMİ BAŞARILI"
    except Exception as e:
        print(e)
        traceback.print_exc()
        deleteDatabase(id)
        deleteImage(id)
        status = False
        message = "YÜZ KAYIT İŞLEMİ BAŞARISIZ"

    return render(
        request,
        "../templates/FaceRecoApp/FaceReco.html",
        {"status": status, "message": message},
    )


# Analiz Sayfasına Veri Göndermek İçin
def analysis(request):
    ref = db.reference("analysis")
    analysis = ref.get()

    return render(
        request,
        "../templates/FaceRecoApp/SentimentAnalysis.html",
        {"analysis": analysis},
    )
