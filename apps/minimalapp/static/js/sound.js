let m5IpAddress = '';

// IPアドレスの保存ボタンのイベントリスナー
document.getElementById('save-ip').addEventListener('click', () => {
    m5IpAddress = document.getElementById('ip-address').value;
    alert('IP Address saved: ' + m5IpAddress);
});

// ブザーのボタンを押したときのイベントリスナー
document.getElementById('buzz-button').addEventListener('click', () => {
    if (!m5IpAddress) {
        alert('Please enter and save the IP address first.');
        return;
    }

    fetch('/buzz', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ip: m5IpAddress })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('M5 Stick C is buzzing!');
        } else {
            alert('Failed to buzz M5 Stick C: ' + data.message);
        }
    })
    .catch(error => {
        alert('Error: ' + error);
    });
});