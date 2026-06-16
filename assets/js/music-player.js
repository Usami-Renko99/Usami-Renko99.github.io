(function () {
  function formatTime(seconds) {
    if (!Number.isFinite(seconds) || seconds < 0) {
      return "0:00";
    }

    var minutes = Math.floor(seconds / 60);
    var remainingSeconds = Math.floor(seconds % 60).toString().padStart(2, "0");
    return minutes + ":" + remainingSeconds;
  }

  function setPlayState(button, isPlaying) {
    button.textContent = isPlaying ? "Pause" : "Play";
    button.setAttribute("aria-label", isPlaying ? "Pause" : "Play");
  }

  function initPlayer(player) {
    var audio = player.querySelector("[data-audio]");

    if (!audio) {
      return;
    }

    var playButton = player.querySelector("[data-play-button]");
    var progress = player.querySelector("[data-progress]");
    var currentTime = player.querySelector("[data-current-time]");
    var duration = player.querySelector("[data-duration]");
    var title = player.querySelector("[data-track-title]");
    var meta = player.querySelector("[data-track-meta]");
    var download = player.querySelector("[data-track-download]");
    var tracks = Array.prototype.slice.call(player.querySelectorAll("[data-track]"));

    function updateProgress() {
      var percent = audio.duration ? (audio.currentTime / audio.duration) * 100 : 0;
      progress.value = percent;
      currentTime.textContent = formatTime(audio.currentTime);
    }

    function updateDuration() {
      duration.textContent = formatTime(audio.duration);
      updateProgress();
    }

    function selectTrack(track, shouldPlay) {
      tracks.forEach(function (item) {
        item.classList.toggle("is-active", item === track);
      });

      audio.src = track.dataset.src;
      title.textContent = track.dataset.title;
      meta.textContent = track.dataset.size || "";

      if (download) {
        download.href = track.dataset.download;
      }

      progress.value = 0;
      currentTime.textContent = "0:00";
      duration.textContent = "0:00";
      audio.load();

      if (shouldPlay) {
        audio.play().catch(function () {
          setPlayState(playButton, false);
        });
      }
    }

    function playNextTrack() {
      var activeIndex = tracks.findIndex(function (track) {
        return track.classList.contains("is-active");
      });
      var nextTrack = tracks[(activeIndex + 1) % tracks.length];

      if (nextTrack) {
        selectTrack(nextTrack, true);
      }
    }

    playButton.addEventListener("click", function () {
      if (audio.paused) {
        audio.play().catch(function () {
          setPlayState(playButton, false);
        });
      } else {
        audio.pause();
      }
    });

    progress.addEventListener("input", function () {
      if (!audio.duration) {
        return;
      }

      audio.currentTime = (Number(progress.value) / 100) * audio.duration;
      updateProgress();
    });

    tracks.forEach(function (track) {
      track.addEventListener("click", function () {
        selectTrack(track, !audio.paused);
      });
    });

    audio.addEventListener("play", function () {
      setPlayState(playButton, true);
    });

    audio.addEventListener("pause", function () {
      setPlayState(playButton, false);
    });

    audio.addEventListener("loadedmetadata", updateDuration);
    audio.addEventListener("timeupdate", updateProgress);
    audio.addEventListener("ended", playNextTrack);
  }

  document.querySelectorAll("[data-music-player]").forEach(initPlayer);
})();
