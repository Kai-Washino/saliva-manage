// キャンバス要素を取得
const canvas = document.getElementById('audio-visualizer');
const canvasCtx = canvas.getContext('2d');

// AudioContextをセットアップ
navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        // マイクストリームをAudioContextに接続
        const source = audioContext.createMediaStreamSource(stream);
        const analyser = audioContext.createAnalyser();

        // FFTサイズを設定（より高い値は細かい解析に使用）
        analyser.fftSize = 2048;
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Float32Array(bufferLength);

        // マイクの音声データをAnalyserに接続
        source.connect(analyser);

        // 1分間のデータを保持するためのバッファを作成
        const sampleRate = 60; // 1秒間に60回サンプリング（表示用のサンプル数）
        const bufferSize = sampleRate * 600; // 60秒間のデータを保持
        const audioBuffer = new Float32Array(bufferSize).fill(0);
        let bufferIndex = 0; // バッファの現在の位置を示すインデックス

        // 音声波形を描画する関数
        function draw() {
            // 描画ループを開始
            requestAnimationFrame(draw);

            // 現在の音声データを取得
            analyser.getFloatTimeDomainData(dataArray);

            // 取得したデータをリングバッファに格納
            for (let i = 0; i < bufferLength; i++) {
                audioBuffer[bufferIndex] = dataArray[i];
                bufferIndex = (bufferIndex + 1) % bufferSize; // インデックスを更新し、リングバッファのように管理
            }

            // キャンバスをクリア
            canvasCtx.fillStyle = 'rgb(240, 240, 240)';
            canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

            // 波形を描画
            canvasCtx.lineWidth = 2;
            canvasCtx.strokeStyle = 'rgb(0, 0, 0)';
            canvasCtx.beginPath();

            const sliceWidth = canvas.width * 1.0 / bufferSize; // 1サンプルあたりのキャンバス幅
            let x = 0; // 描画のX座標を初期化

            // バッファからデータを取り出し、波形を描画
            for (let i = 0; i < bufferSize; i++) {
                const v = audioBuffer[(bufferIndex + i) % bufferSize];
                const y = (v + 1) * canvas.height / 2; // 値をキャンバスの高さに正規化

                if (i === 0) {
                    canvasCtx.moveTo(x, y); // 最初の点を移動
                } else {
                    canvasCtx.lineTo(x, y); // 次の点に線を描画
                }

                x += sliceWidth; // X座標を次に進める
            }

            canvasCtx.lineTo(canvas.width, canvas.height / 2);
            canvasCtx.stroke(); // 描画を完了
        }

        // 描画を開始
        draw();
    })
    .catch(function(err) {
        // マイクアクセスに失敗した場合のエラー処理
        console.error('The following error occurred: ' + err);
    });