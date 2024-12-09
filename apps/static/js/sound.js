let m5IpAddress = '';

// IPアドレスの保存ボタンのイベントリスナー
document.getElementById('save-ip').addEventListener('click', () => {
    m5IpAddress = document.getElementById('ip-address').value;
    alert('IP Address saved: ' + m5IpAddress);
});

// ブザーのボタンを押したときのイベントリスナー
document.getElementById('buzz-button').addEventListener('click', () => {
    buzzM5StickC();
});

// 条件づけのボタンを押したときのイベントリスナー
document.getElementById('conditioning-button').addEventListener('click', () => {
    if (!m5IpAddress) {
        alert('IPアドレスを入力してください');
        return;
    }

    fetch('/sound/conditioning', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ip: m5IpAddress })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // alert('M5 Stick C is buzzing!');
        } else {
            alert('失敗: ' + data.message);
        }
    })
    .catch(error => {
        alert('Error: ' + error);
    });
});

// 咀嚼認識時のイベントリスナー
function triggerSoundOnMastication() {
    console.log("function start")
    fetch('/display/is_mastication')
        .then(response => response.json())
        .then(data => {
            if (data.is_mastication) {
                buzzM5StickC(); // 音を鳴らす関数を呼び出し
            }
        })
        .catch(error => console.error('Error fetching mastication status:', error));
}

function buzzM5StickC() {
    if (!m5IpAddress) {
        alert('IPアドレスを入力してください');
        return;
    }

    fetch('/sound/buzz', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ip: m5IpAddress })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('M5 Stick C is buzzing!');
        } else {
            alert('失敗: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error buzzing M5 Stick C:', error);
    });
}
