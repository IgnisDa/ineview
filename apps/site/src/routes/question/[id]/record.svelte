<script context="module">
  import { goto } from '$app/navigation';
  import { httpService } from '$lib/http';
  import NProgress from 'nprogress';
  import { onMount } from 'svelte';
  import { questions, questions_set } from '../../../stores';

  /** @type {import('@sveltejs/kit').Load} */
  export async function load({ params }) {
    try {
      const { data } = await httpService.get(
        `/questions/questions/${params.id}`
      );
      return { props: { details: data } };
    } catch {
      return { error: 'This question does not exist', status: 404 };
    }
  }
</script>

<script lang="ts">
  export let details;

  enum Stages {
    Permission = 'Testing video and audio...',
    InitialDetails = 'Initial details',
    Thinking = 'Time to think',
    Recording = 'Cameras rolling',
  }

  let stage = Stages.Permission;

  let thinking_duration = details.thinking_duration;
  let answer_duration = details.answer_duration;
  const question = details.text;
  const description = details.description;

  let stream: MediaStream;
  let recorder: MediaRecorder;
  let video: HTMLVideoElement;

  let timer: number | null;

  let countdown = 5;

  onMount(async () => {
    $questions = $questions.slice(1);
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true,
    });
    stream.getTracks().forEach((track) => track.stop());
    setTimeout(() => {
      timer = setInterval(() => (countdown -= 1), 1000);
      stage = Stages.InitialDetails;
    }, 1500);
  });

  $: {
    if (countdown === 0) {
      clearInterval(timer);
      if (stage === Stages.InitialDetails) {
        countdown = thinking_duration;
        timer = setInterval(() => (countdown -= 1), 1000);
        stage = Stages.Thinking;
      } else if (stage === Stages.Thinking) {
        countdown = answer_duration;
        timer = setInterval(() => (countdown -= 1), 1000);
        stage = Stages.Recording;
        startRecording();
      } else if (stage === Stages.Recording) {
        stage = Stages.Recording;
        stopRecording();
      }
    }
  }

  const startRecording = async () => {
    stream = await navigator.mediaDevices.getUserMedia({
      video: true,
      audio: true,
    });
    video.srcObject = stream;
    recorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
    recorder.start();
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
    video.srcObject = undefined;
  };

  const startProcessing = async (videoId: number) => {
    const { data } = await httpService.post<{ status: boolean }>(
      `/video/process/${videoId}`
    );
    if (!data.status)
      alert('There was an error while processing your video, please try again');
    else {
      if ($questions.length > 0) {
        location.assign(`/question/${$questions[0]}/record`);
      } else {
        // TODO: Redirect to `/attempt` page
        goto(`/questions-set/${$questions_set}/stats`);
        $questions_set = null;
        $questions = null;
      }
    }
  };
</script>

<div
  class="flex flex-col space-y-10 flex-1 text-white items-center justify-center"
>
  {#if stage === Stages.Permission}
    <div class="text-4xl">{stage}</div>
  {:else}
    <div class="text-6xl">{stage}: {countdown}</div>
    <div class="flex flex-col">
      <span class="text-2xl underline">{question}</span>
      <span class="text-lg">{description}</span>
    </div>
    {#if stage === Stages.Recording}
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
    {/if}
  {/if}
</div>
