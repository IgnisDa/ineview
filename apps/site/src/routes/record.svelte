<script lang="ts">
  import { goto } from '$app/navigation';
  import { variables } from '$lib/environment';
  import RecordButton from '$lib/components/record/RecordButton.svelte';
  import { httpService } from '$lib/http';
  import NProgress from 'nprogress';

  let stream: MediaStream;
  let recorder: MediaRecorder;
  let video: HTMLVideoElement;

  let countdown = variables.countdownTimer;

  let timer: number | null;

  $: {
    if (countdown === 0)
      if (timer) {
        clearInterval(timer);
        stopRecording();
        timer = null;
      }
  }

  let isStartBtnDisabled = false;

  const startRecording = async () => {
    const stm = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true,
    });
    stream = stm;
    video.srcObject = stream;
    recorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
    recorder.start();
    timer = setInterval(() => (countdown -= 1), 1000);
    isStartBtnDisabled = true;
  };

  const stopRecording = () => {
    recorder.ondataavailable = async (e) => {
      let form = new FormData();
      form.append('file', e.data);
      NProgress.start();
      const { data } = await httpService.post<{ id: number }>(
        '/video/upload/',
        form,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      await startProcessing(data.id);
      NProgress.done();
    };
    recorder.stop();
    stream.getTracks().forEach((track) => track.stop());
    isStartBtnDisabled = false;
    video.srcObject = undefined;
  };

  const startProcessing = async (videoId: number) => {
    const { data } = await httpService.post<{ status: boolean }>(
      `/video/process/${videoId}`
    );
    if (!data.status)
      alert('There was an error while processing your video, please try again');
    else {
      goto(`/stats/video-${videoId}`);
    }
  };
</script>

<div class="flex flex-col space-y-10 flex-1 items-center md:justify-center">
  <div class="flex pt-6 z-10 justify-around md:pt-0 md:right-4 md:fixed">
    <RecordButton
      on:click={startRecording}
      isDisabled={isStartBtnDisabled}
      timer={countdown}
    />
  </div>
  <div class="flex items-center justify-center">
    <div
      class="rounded-lg bg-gray-800 h-400px w-96 relative md:h-700px md:w-800px"
    >
      <video
        autoplay
        muted
        bind:this={video}
        class="bg-cover h-auto min-w-full min-h-full w-auto right-0 bottom-0 absolute overflow-hidden"
      />
    </div>
  </div>
</div>

<style>
  @import 'nprogress/nprogress.css';
</style>
