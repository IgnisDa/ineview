<script lang="ts">
  import { goto } from '$app/navigation';
  import NProgress from 'nprogress';
  import 'nprogress/nprogress.css';
  import { httpService } from '$lib/http';

  let stream: MediaStream;
  let recorder: MediaRecorder;
  let video: HTMLVideoElement;

  let isStopBtnDisabled = true;
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
    isStartBtnDisabled = true;
    isStopBtnDisabled = false;
  };

  const stopRecording = () => {
    recorder.ondataavailable = async (e) => {
      let form = new FormData();
      form.append('file', e.data);
      NProgress.start();
      const { data } = await httpService.post<{ id: number }>(
        '/video/upload/',
        form,
        {
          headers: { 'Content-Type': 'multipart/form-data' },
        }
      );
      await startProcessing(data.id);
      NProgress.done();
    };
    recorder.stop();
    stream.getTracks().forEach((track) => track.stop());
    isStartBtnDisabled = false;
    isStopBtnDisabled = true;
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

<div class="flex flex-col space-y-10 p-6">
  <div class="flex justify-around">
    <button
      disabled={isStartBtnDisabled}
      class="rounded-lg bg-warm-gray-700 p-2 ring-4 text-red-50 disabled:bg-warm-gray-400"
      on:click={startRecording}
    >
      Start Recording
    </button>
    <button
      class="rounded-lg  bg-warm-gray-700 p-2 ring-4 text-red-50 disabled:bg-warm-gray-400"
      disabled={isStopBtnDisabled}
      on:click={stopRecording}
    >
      Stop Recording
    </button>
  </div>
  <div class="flex items-center justify-center">
    <div class="rounded-lg bg-gray-800 h-700px w-800px relative">
      <video
        autoplay
        muted
        bind:this={video}
        class="bg-cover h-auto min-w-full min-h-full w-auto right-0 bottom-0 absolute overflow-hidden"
      />
    </div>
  </div>
</div>
