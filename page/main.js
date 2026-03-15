const FRAME_RATE = 30;

let asciiFrames = null; // アスキーアートのフレームを格納する変数
let animationInterval = null; // アニメーションのID

/**
 * asciiart_database.jsから呼び出されるコールバック関数
 * ページ読み込み時に自動で実行され、データを変数に格納する
 * @param {object} data - 読み込まれたJSONデータ
 */
function loadData(data) {
    if (data && data.frames) {
        asciiFrames = data.frames;
        //console.log(`データ読み込み完了。${asciiFrames.length}フレーム。再生準備OK`);
        //console.log("コンソールで play() を実行してください。");
    } else {
        console.error('データの読み込みに失敗しました。');
    }
}

/**
 * コンソールから実行するための再生開始関数
 */
function play() {
    if (!asciiFrames) {
        console.error('再生データがありません。');
        return;
    }

    let frameIndex = 0;

    // 実行中のアニメーションがあれば停止
    if (animationInterval) {
        clearInterval(animationInterval);
    }

    // console.log('--- 再生開始 ---');

    animationInterval = setInterval(() => {
        //console.clear();
        // frameIndexをnで割った余りが0のとき (＝nフレームごと) にコンソールをクリア
        if (frameIndex % 1200 === 0) {
            console.clear();
        }
        console.log(asciiFrames[frameIndex]);
        frameIndex++;

        if (frameIndex >= asciiFrames.length) {
            clearInterval(animationInterval);
            // console.log('--- fin ---');
        }
    }, 1000 / FRAME_RATE);
}
