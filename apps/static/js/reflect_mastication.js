// 咀嚼カウントを定期的にサーバーから取得して表示を更新する
function updateMasticationCount() {
    fetch('/display/mastication_count')
        .then(response => response.json())
        .then(data => {
            document.getElementById('mastication-count').textContent = data.mastication_count;
        })
        .catch(error => console.error('Error fetching mastication count:', error));
}

// 咀嚼カウントを定期的にサーバーから取得して表示を更新する
function updateMasticationStatus() {
    fetch('/display/is_mastication')
        .then(response => response.json())
        .then(data => {
            document.getElementById('mastication-status').textContent = data.is_mastication;
        })
        .catch(error => console.error('Error fetching mastication count:', error));
}

// 2秒ごとに更新
// setInterval(updateMasticationCount, 2000);

setInterval(updateMasticationStatus, 1000);