(function () {
    const FRAME_RATE = 30;
    const FRAME_DURATION = 1000 / FRAME_RATE;

    let asciiFrames = null;
    let animationId = null;
    let isPlaying = false;

    // データ読み込み用コールバック
    window.loadData = function (data) {
        if (data && Array.isArray(data.frames)) {
            asciiFrames = data.frames;
        } else {
            console.error('[Error] Invalid data format');
        }
    };

    // 再生開始
    window.play = function () {
        if (!asciiFrames) return console.error('[Error] Data not loaded');
        if (isPlaying) return;

        isPlaying = true;
        let startTime = performance.now();
        let lastRenderedFrame = -1;

        function loop(currentTime) {
            if (!isPlaying) return;

            const elapsedTime = currentTime - startTime;
            const currentFrameIndex = Math.floor(elapsedTime / FRAME_DURATION);

            if (currentFrameIndex >= asciiFrames.length) {
                isPlaying = false;
                animationId = null;
                return;
            }

            if (currentFrameIndex > lastRenderedFrame) {
                // 1200フレームごとにクリア
                if (currentFrameIndex > 0 && currentFrameIndex % 1200 === 0) {
                    console.clear();
                }
                console.log(asciiFrames[currentFrameIndex]);
                lastRenderedFrame = currentFrameIndex;
            }

            animationId = requestAnimationFrame(loop);
        }
        animationId = requestAnimationFrame(loop);
    };

    // 停止
    window.stop = function () {
        if (isPlaying && animationId !== null) {
            cancelAnimationFrame(animationId);
            isPlaying = false;
            animationId = null;
            console.log('=== Stopped ===');
        }
    };
})();
