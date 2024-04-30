const audioPlayer = document.getElementById('audioPlayer');
const playlist = document.getElementsByClassName('track'); // список треков
let currentTrackIndex = 0; // индекс текущего трека

audioPlayer.addEventListener('timeupdate', function() {
    localStorage.setItem('page', audioPlayer.src);
    localStorage.setItem('audioProgress', audioPlayer.currentTime);
	localStorage.setItem('index', currentTrackIndex);
});

audioPlayer.addEventListener('ended', function() {
  // Автоматически переключаемся на следующий трек в плейлисте
  currentTrackIndex++;
  if (currentTrackIndex < playlist.length) {
    changeTrack(playlist[currentTrackIndex].name, playlist[currentTrackIndex].innerHTML, currentTrackIndex); // переключаемся на следующий трек
  }
});

// Загружаем сохраненное время воспроизведения
window.onload = function() {
	audioPlayer.playbackRate = 2
    if(localStorage.getItem('page')) {
        audioPlayer.src = localStorage.getItem('page');
      }
	if(localStorage.getItem('index')) {
        currentTrackIndex = localStorage.getItem('index');
    }
    if(localStorage.getItem('audioProgress')) {
        audioPlayer.currentTime = localStorage.getItem('audioProgress');
    }
    if(localStorage.getItem('name')) {
        document.getElementById('number').innerHTML = localStorage.getItem('name');
    }
}

function changeTrack(trackUrl, name, id) {
  audioPlayer.src = trackUrl;
  audioPlayer.playbackRate = 2
  audioPlayer.play();
  currentTrackIndex = id;
  document.getElementById('number').innerHTML = name;
  localStorage.setItem('index', currentTrackIndex);
  localStorage.setItem('page', audioPlayer.src);
  localStorage.setItem('name', name);
  localStorage.setItem('audioProgress', 0); // Сбрасываем сохраненное время при смене трека
}

function skip(time) {
  audioPlayer.currentTime += time;
  localStorage.setItem('audioProgress', audioPlayer.currentTime);
}

function changeSpeed(speed) {
  audioPlayer.playbackRate = speed;
}
