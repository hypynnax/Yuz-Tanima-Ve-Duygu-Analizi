//Panel Açma / Kapatma İşlemleri
const leftPanel = document.getElementById('left-panel');
const rightPanel = document.getElementById('right-panel');
const leftButton = document.getElementById('left-button');
const rightButton = document.getElementById('right-button');
const leftContent = document.getElementById('faceReco-wrapper');
const rightContent = document.getElementById('faceRec-wrapper');
let isLeftOpen = false;
let isRightOpen = false;

leftPanel.addEventListener('click', () => {
    leftPanel.style.flex = '2';
    rightPanel.style.flex = '0';
    leftPanel.classList.remove('active');
    rightPanel.classList.add('active');
    leftButton.style.display = 'none';
    leftContent.style.display = 'flex';
    rightButton.style.transform = 'rotate(90deg)';
    rightButton.style.display = 'block';
    rightContent.style.display = 'none';
    rightButton.style.width = '141px';
    if (!isLeftOpen) {
        openLeftCamera(true);
        isLeftOpen = true;
        sendPhoto();
    }
    if (isRightOpen) {
        openRightCamera(false);
        isRightOpen = false;
    }
});

rightPanel.addEventListener('click', () => {
    leftPanel.style.flex = '0';
    rightPanel.style.flex = '2';
    leftPanel.classList.add('active');
    rightPanel.classList.remove('active');
    leftButton.style.transform = 'rotate(-90deg)';
    leftButton.style.display = 'block';
    leftContent.style.display = 'none';
    rightButton.style.display = 'none';
    rightContent.style.display = 'flex';
    leftButton.style.width = '167px';
    if (isLeftOpen) {
        openLeftCamera(false);
        isLeftOpen = false;
    }
    if (!isRightOpen) {
        openRightCamera(true);
        isRightOpen = true;
    }
});
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//Tema Ayarlama
const standardTheme = document.getElementById('standard');
const lightTheme = document.getElementById('light');
const darkerTheme = document.getElementById('darker');
const box = document.getElementById('info-content');

standardTheme.addEventListener('click', () => {
    box.style.backgroundColor = 'rgba(255, 255, 255, 0)';
    box.style.color = "#05FF04";
    box.style.border = '1px solid rgba(255, 255, 255, 0)';
});

lightTheme.addEventListener('click', () => {
    box.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
    box.style.color = "#FFFFFF";
    box.style.border = '1px dashed #FFFFFF';
});

darkerTheme.addEventListener('click', () => {
    box.style.backgroundColor = '#000000';
    box.style.color = "#05FF04";
    box.style.border = '1px solid #05FF04';
});
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//Timer İşlemleri
let timerElement = document.getElementById('camera-time');
let startTime;
let timerInterval;

function updateTimer() {
    let elapsedTime = Date.now() - startTime;
    let totalSeconds = Math.floor(elapsedTime / 1000);
    let hours = Math.floor(totalSeconds / 3600);
    let minutes = Math.floor((totalSeconds % 3600) / 60);
    let seconds = totalSeconds % 60;

    hours = String(hours).padStart(2, '0');
    minutes = String(minutes).padStart(2, '0');
    seconds = String(seconds).padStart(2, '0');

    timerElement.textContent = `${hours}:${minutes}:${seconds}`;
}

function startTimer() {
    startTime = Date.now();
    timerInterval = setInterval(updateTimer, 1000);
}

function resetTimer() {
    clearInterval(timerInterval);
    timerElement.textContent = '00:00:00';
}
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//Fotoğrafları Anlık Olarak Back-End Gönderme
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var left_name = document.getElementById('left_name');
var left_surname = document.getElementById('left_surname');
var left_dateOfBirth = document.getElementById('left_dateOfBirth');
var left_bloodGroup = document.getElementById('left_bloodGroup');
var left_job = document.getElementById('left_job');
var left_size = document.getElementById('left_size');
var left_weight = document.getElementById('left_weight');
var left_age = document.getElementById('left_age');
var left_gender = document.getElementById('left_gender');
var canvasWidth = 640;
var canvasHeight = 480;

function sendPhoto() {
    if (isLeftOpen) {
        setTimeout(() => {
            sendWithAjax();
            sendPhoto();
        }, 2000);
    }
}

async function sendWithAjax() {
    context.clearRect(0, 0, canvasWidth, canvasHeight);
    context.save();
    context.scale(-1, 1);
    context.drawImage(cameraReco, -canvasWidth, 0, canvasWidth, canvasHeight);
    context.restore();
    var dataURL = canvas.toDataURL('image/png');
    var formData = new FormData();
    formData.append('file', dataURL);
    $.ajax({
        url: 'http://127.0.0.1:8000/face/Reco/',
        type: 'POST',
        processData: false,
        contentType: false,
        data: formData,
        success: function (result) {
            left_name.textContent = result.name;
            left_surname.textContent = result.surname;
            left_dateOfBirth.textContent = result.dateOfBirth;
            left_bloodGroup.textContent = result.bloodGroup;
            left_job.textContent = result.job;
            left_size.textContent = result.size;
            left_weight.textContent = result.weight;
            left_age.textContent = result.age;
            left_gender.textContent = result.gender;
        },
        error: () => {
            left_name.textContent = "--";
            left_surname.textContent = "--";
            left_dateOfBirth.textContent = "--/--/----";
            left_bloodGroup.textContent = "--";
            left_job.textContent = "--";
            left_size.textContent = "--";
            left_weight.textContent = "--";
            left_age.textContent = "--";
            left_gender.textContent = "--";
        }
    });
}
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//Kamera Açma / Kapatma İşlemleri
const cameraReco = document.getElementById('cameraReco');
const cameraRec = document.getElementById('cameraRec');
const rightCamera = document.getElementById('right-camera');
let cameraOpen = true;
let stream;

function openCamera(camera) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(mediaStream => {
            stream = mediaStream;
            camera.srcObject = stream;
            camera.play();
        })
        .catch(error => {
            console.error("Kamera erişim hatası: ", error);
        });
}

function closeCamera(camera) {
    if (stream) {
        let tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        camera.srcObject = null;
        stream = null;
    }
}

function openLeftCamera(isOpen) {
    if (isOpen) {
        openCamera(cameraReco);
    } else {
        closeCamera(cameraReco);
    }
}

function openRightCamera(isOpen) {
    if (isOpen) {
        openCamera(cameraRec);
        rightCamera.classList.add('shutonEffect');
        rightCamera.classList.remove('shutoffEffect');
        startTimer();
        cameraOpen = true;
    } else {
        rightCamera.classList.add('shutoffEffect');
        rightCamera.classList.remove('shutonEffect');
        closeCamera(cameraRec);
        resetTimer();
        cameraOpen = false;
    }
}
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

// Sağ Kamerayı Başlat / Durdur İşlemleri
const stopButton = document.getElementById('stop');
const playButton = document.getElementById('play');

stopButton.addEventListener('click', () => {
    if (cameraOpen) {
        openRightCamera(false);
    }
});

playButton.addEventListener('click', () => {
    if (!cameraOpen) {
        openRightCamera(true);
    }
});
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//Resim Çekme ve Çerçevelere Koyma İşlemleri
const shutterButton = document.getElementById('shutter');
const messageBox = document.getElementById("messageBox");
const photos = [
    {
        img: document.getElementById('photo-one'),
        deleteButton: document.getElementById('delete-one'),
        addButton: document.getElementById('add-one'),
        imgInput: document.getElementById('photoOne'),
        context: null,
        check: false
    },

    {
        img: document.getElementById('photo-two'),
        deleteButton: document.getElementById('delete-two'),
        addButton: document.getElementById('add-two'),
        imgInput: document.getElementById('photoTwo'),
        context: null,
        check: false
    },

    {
        img: document.getElementById('photo-three'),
        deleteButton: document.getElementById('delete-three'),
        addButton: document.getElementById('add-three'),
        imgInput: document.getElementById('photoThree'),
        context: null,
        check: false
    },
];

photos.forEach(photo => {
    photo.context = photo.img.getContext('2d');
    photo.deleteButton.addEventListener('click', () => {
        if (photo.check) {
            photo.img.style.display = "none";
            photo.deleteButton.style.display = "none";
            photo.addButton.style.display = "flex";
            photo.check = false;
            for (let i = 0; i < photos.length; i++) {
                if (photos[i].check) {
                    return;
                }
            };
            messageBox.style.display = "flex";
        }
    });

    ['mouseover', 'mouseout', 'mousedown', 'mouseup'].forEach(event => {
        photo.deleteButton.addEventListener(event, () => {
            const state = event === 'mousedown' ? 'active' : (event === 'mouseover' || event === 'mouseup') ? 'hover' : '';
            photo.deleteButton.style.backgroundImage = `url('../../static/FaceRecoApp/img/delete${state}.png')`;
        });
    });
});

shutterButton.addEventListener('click', () => {
    if (cameraOpen) {
        const { width: canvasWidth, height: canvasHeight } = photos[0].img;
        for (let i = 0; i < photos.length; i++) {
            const photo = photos[i];
            if (!photo.check) {
                photo.context.clearRect(0, 0, canvasWidth, canvasHeight);
                photo.context.save();
                photo.context.scale(-1, 1);
                photo.context.drawImage(cameraRec, -canvasWidth, 0, canvasWidth, canvasHeight);
                photo.context.restore();
                photo.imgInput.value = photo.img.toDataURL('image/png');
                photo.img.style.display = "block";
                photo.deleteButton.style.display = "flex";
                photo.addButton.style.display = "none";
                photo.check = true;
                messageBox.style.display = "none";
                return;
            }
        };
    }
});
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//Girdi İşlemleri
const elements = [
    'right_name',
    'right_surname',
    'right_date_of_birth',
    'right_job',
    'right_size',
    'right_weight',
    'right_blood_group_drop_box',
    'right_gender_drop_box'
];

function addInputListeners(element) {
    element.addEventListener('focus', () => {
        element.classList.add('input-focus');
    });

    element.addEventListener('blur', () => {
        if (element.value === "") {
            element.classList.remove('input-focus');
        }
    });

    element.addEventListener('mouseenter', () => {
        element.classList.add('input-hover');
    });

    element.addEventListener('mouseleave', () => {
        element.classList.remove('input-hover');
    });
}

elements.forEach(id => {
    const element = document.getElementById(id);
    addInputListeners(element);
});
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//Doğum Tarihini Formatlama
function formatDate(value) {
    let formattedValue = value.replace(/\D/g, '');

    if (formattedValue.length > 2) {
        formattedValue = formattedValue.slice(0, 2) + '/' + formattedValue.slice(2);
    }

    if (formattedValue.length > 5) {
        formattedValue = formattedValue.slice(0, 5) + '/' + formattedValue.slice(5);
    }

    return formattedValue.slice(0, 10);
}

const rightDateOfBirth = document.getElementById(elements[2]);
rightDateOfBirth.addEventListener('input', () => {
    const originalValue = rightDateOfBirth.value;
    rightDateOfBirth.value = formatDate(originalValue);
});
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//Yüz Kayıt Formunun İncelenmesi Ve Submit Edilmesi
function submitFormRec() {
    var dateOfBirth = document.getElementById('right_date_of_birth').value;

    if (!photos[0].check || !photos[1].check || !photos[2].check) {
        showMessage("Tüm Resimleri Tamamlayınız.", rightPanel, false);
        return false;
    }

    if (dateOfBirth.length != 10) {
        showMessage("Lütfen Doğum Tarihini Doğru Formatta Eksiksiz Yazın!", rightPanel, false);
        return false;
    }

    return true;
};
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

//Hata Mesajı Gösterme Fonksiyonu
function showMessage(message, element, isSuccess, time = 3000) {
    var messageBox = document.createElement("div");
    messageBox.textContent = message;
    messageBox.classList.add("info");

    if (isSuccess) {
        messageBox.classList.add("info-success");
    } else {
        messageBox.classList.add("info-error");
    }

    element.appendChild(messageBox);
    setTimeout(() => {
        element.removeChild(messageBox);
    }, time);
}
