// script.js
$(document).ready(function () {
  let mediaRecorder;
  let recordedBlobs = [];

  const video = document.getElementById('video');
  const startRecordingBtn = document.getElementById('startRecording');
  const stopRecordingBtn = document.getElementById('stopRecording');
  const previewRecordingBtn = document.getElementById('previewRecording');
  const redoRecordingBtn = document.getElementById('redoRecording');
  const cancelRecordingBtn = document.getElementById('cancelRecording');
  const nextQuestionBtn = document.getElementById('nextQuestion');
  const videoDataInput = document.getElementById('videoData');

  startRecordingBtn.addEventListener('click', startRecording);
  stopRecordingBtn.addEventListener('click', stopRecording);
  previewRecordingBtn.addEventListener('click', previewRecording);
  redoRecordingBtn.addEventListener('click', redoRecording);
  cancelRecordingBtn.addEventListener('click', cancelRecording);
  nextQuestionBtn.addEventListener('click', goToNextQuestion);

  function startRecording() {
      navigator.mediaDevices.getUserMedia({ video: true, audio: true })
          .then(handleSuccess)
          .catch(handleError);

      startRecordingBtn.classList.add('d-none');
      stopRecordingBtn.classList.remove('d-none');
  }

  function handleSuccess(stream) {
      video.srcObject = stream;
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = handleDataAvailable;
      mediaRecorder.start();
  }

  function handleDataAvailable(event) {
      if (event.data && event.data.size > 0) {
          recordedBlobs.push(event.data);
      }
  }

  function stopRecording() {
      mediaRecorder.stop();
      stopRecordingBtn.classList.add('d-none');
      previewRecordingBtn.classList.remove('d-none');
      redoRecordingBtn.classList.remove('d-none');
      cancelRecordingBtn.classList.remove('d-none');
      nextQuestionBtn.classList.add('d-none');
  }

  function previewRecording() {
      const superBuffer = new Blob(recordedBlobs, { type: 'video/webm' });
      video.src = window.URL.createObjectURL(superBuffer);
      video.controls = true;
      video.play();
  }

  function redoRecording() {
      video.srcObject.getTracks().forEach(track => track.stop());
      recordedBlobs = [];
      video.src = '';
      video.controls = false;
      startRecordingBtn.classList.remove('d-none');
      previewRecordingBtn.classList.add('d-none');
      redoRecordingBtn.classList.add('d-none');
      cancelRecordingBtn.classList.add('d-none');
      nextQuestionBtn.classList.remove('d-none');
  }

  function cancelRecording() {
      video.srcObject.getTracks().forEach(track => track.stop());
      recordedBlobs = [];
      video.src = '';
      video.controls = false;
      startRecordingBtn.classList.remove('d-none');
      stopRecordingBtn.classList.add('d-none');
      previewRecordingBtn.classList.add('d-none');
      redoRecordingBtn.classList.add('d-none');
      cancelRecordingBtn.classList.add('d-none');
      nextQuestionBtn.classList.remove('d-none');
  }

  function goToNextQuestion() {
      document.getElementById('questionForm').submit();
  }

  function handleError(error) {
      console.error('Error: ', error);
  }

  // Send recorded video data to server when form is submitted
  $('#questionForm').on('submit', function (event) {
      event.preventDefault();
      const blob = new Blob(recordedBlobs, { type: 'video/webm' });
      const reader = new FileReader();
      reader.onloadend = function () {
          const videoData = reader.result;
          videoDataInput.value = videoData;
          this.form.submit();
      };
      reader.readAsArrayBuffer(blob);
  });
});
