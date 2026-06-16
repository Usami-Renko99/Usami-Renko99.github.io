(function () {
  var storageKey = "renkoMusicPlayerState";

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

  function readState() {
    try {
      return JSON.parse(window.localStorage.getItem(storageKey)) || {};
    } catch (error) {
      return {};
    }
  }

  function writeState(state) {
    try {
      window.localStorage.setItem(storageKey, JSON.stringify(state));
    } catch (error) {
      return;
    }
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
    var toggleButton = player.querySelector("[data-player-toggle]");
    var tracks = Array.prototype.slice.call(player.querySelectorAll("[data-track]"));
    var pendingSeek = 0;
    var lastSavedSecond = -1;
    var shouldAutoResume = false;

    function getActiveTrack() {
      return tracks.find(function (track) {
        return track.classList.contains("is-active");
      }) || tracks[0];
    }

    function saveState() {
      var activeTrack = getActiveTrack();
      var roundedTime = Math.floor(audio.currentTime || 0);

      writeState({
        src: activeTrack ? activeTrack.dataset.src : audio.getAttribute("src"),
        currentTime: roundedTime,
        expanded: player.classList.contains("is-expanded"),
        wasPlaying: !audio.paused
      });
    }

    function tryAutoResume() {
      if (!shouldAutoResume) {
        return;
      }

      shouldAutoResume = false;
      audio.play().catch(function () {
        setPlayState(playButton, false);
      });
    }

    function setExpanded(isExpanded, shouldSave) {
      player.classList.toggle("is-expanded", isExpanded);

      if (toggleButton) {
        toggleButton.textContent = isExpanded ? "Close" : "List";
        toggleButton.setAttribute("aria-expanded", String(isExpanded));
      }

      if (shouldSave) {
        saveState();
      }
    }

    function updateProgress() {
      var percent = audio.duration ? (audio.currentTime / audio.duration) * 100 : 0;
      progress.value = percent;
      currentTime.textContent = formatTime(audio.currentTime);

      var currentSecond = Math.floor(audio.currentTime || 0);
      if (currentSecond !== lastSavedSecond && currentSecond % 5 === 0) {
        lastSavedSecond = currentSecond;
        saveState();
      }
    }

    function updateDuration() {
      duration.textContent = formatTime(audio.duration);

      if (pendingSeek && audio.duration) {
        audio.currentTime = Math.min(pendingSeek, Math.max(audio.duration - 0.5, 0));
        pendingSeek = 0;
      }

      updateProgress();
      tryAutoResume();
    }

    function selectTrack(track, shouldPlay, shouldSave) {
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

      if (shouldSave !== false) {
        saveState();
      }

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
      saveState();
    });

    tracks.forEach(function (track) {
      track.addEventListener("click", function () {
        selectTrack(track, !audio.paused);
      });
    });

    audio.addEventListener("play", function () {
      setPlayState(playButton, true);
      saveState();
    });

    audio.addEventListener("pause", function () {
      setPlayState(playButton, false);
      saveState();
    });

    audio.addEventListener("loadedmetadata", updateDuration);
    audio.addEventListener("timeupdate", updateProgress);
    audio.addEventListener("ended", playNextTrack);

    if (toggleButton) {
      toggleButton.addEventListener("click", function () {
        setExpanded(!player.classList.contains("is-expanded"), true);
      });
    }

    window.addEventListener("beforeunload", saveState);

    var savedState = readState();
    var savedTrack = tracks.find(function (track) {
      return track.dataset.src === savedState.src;
    });

    setExpanded(Boolean(savedState.expanded), false);

    if (Number(savedState.currentTime) > 0) {
      pendingSeek = Number(savedState.currentTime);
    }

    shouldAutoResume = Boolean(savedState.wasPlaying);

    if (savedTrack) {
      selectTrack(savedTrack, false, false);
    } else {
      audio.load();
    }
  }

  document.querySelectorAll("[data-music-player]").forEach(initPlayer);
})();
