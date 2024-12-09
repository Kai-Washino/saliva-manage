let audioContext;
let analyser;
let dataArray;
let recording = false;
let isMeasuring = false;

console.log(isMeasuring)

// ボタンのクリックイベント
document.getElementById('measure-button').addEventListener('click', function() {
    // フラグを反転
    isMeasuring = !isMeasuring;

    // ボタンのテキストと色を変更
    if (isMeasuring) {
        this.textContent = '計測中...';
        this.classList.remove('btn-primary');
        this.classList.add('btn-danger');        
    } else {
        this.textContent = '計測開始';
        this.classList.remove('btn-danger');
        this.classList.add('btn-primary');        
        stopAudio();
    }
});

navigator.mediaDevices.getUserMedia({ audio: true })
.then(function(stream) {        
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const source = audioContext.createMediaStreamSource(stream);
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 2048;
        dataArray = new Float32Array(analyser.fftSize);

        source.connect(analyser);       
        detectSound(stream);
         
        
})
.catch(function(err) {
    console.error('The following error occurred: ' + err);
});

// 音の検出を行う関数
function detectSound(stream) {
    requestAnimationFrame(() => detectSound(stream));
    analyser.getFloatTimeDomainData(dataArray);

    // 音のレベルを判定（閾値を超えたら録音を開始）
    const rms = Math.sqrt(dataArray.reduce((sum, val) => sum + val * val, 0) / dataArray.length);
    if (rms > thresholdValue && !recording && isMeasuring) {        
        recording = true;
        recordAudio(stream);        
    }
}

// 1秒間の音を録音してFlaskに送信
function recordAudio(stream) {
    console.log("record start");
    const recorder = new MediaRecorder(stream);
    
    recorder.ondataavailable = function(event) {
        console.log(event.data.size);
        if (event.data.size > 0) {            
            sendAudioToServer(event.data);
        }
    };

    recorder.start();
    setTimeout(() => {
        recorder.stop();
        console.log("record stop");
        recording = false;
    }, 1000); // 1秒間録音
}

// Flaskサーバーに音声データを送信
function sendAudioToServer(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio.wav');
    console.log("send audio");

    fetch('/processing/receive_audio', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);        
    })
    .catch(error => {
        console.error('Error:', error);        
    });
}

function stopAudio() {
    fetch('/processing/stop_measurement', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: 'stop' })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}