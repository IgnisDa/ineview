<script lang="ts">
  let stream: MediaStream;
  let recorder: MediaRecorder;
  let video: HTMLVideoElement;

  let isStopBtnDisabled = true;
  let isStartBtnDisabled = false;

  let videos = Array<{ filename: string; href: string }>();

  const startRecording = async () => {
    const stm = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true,
    });
    stream = stm;
    video.srcObject = stream;
    recorder = new MediaRecorder(stream, {
      mimeType: 'video/webm',
    });
    recorder.start();
    isStartBtnDisabled = true;
    isStopBtnDisabled = false;
  };

  const stopRecording = () => {
    recorder.ondataavailable = (e) => {
      const filename = ['video_', new Date().toISOString(), '.webm'].join('');
      const href = URL.createObjectURL(e.data);
      videos = [...videos, { filename, href }];
    };
    recorder.stop();
    stream.getTracks().forEach((track) => track.stop());
    isStartBtnDisabled = false;
    isStopBtnDisabled = true;
    video.srcObject = undefined;
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
  {#if videos.length > 0}
    <div>
      <span>Downloads List:</span>
      <ul>
        {#each videos as video}
          <li>
            <a href={video.href} download={video.filename}>{video.filename}</a>
          </li>
        {/each}
      </ul>
    </div>
  {/if}
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
