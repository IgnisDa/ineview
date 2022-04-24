<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { httpService } from '$lib/http';
  import { Loading } from 'carbon-components-svelte';
  import NProgress from 'nprogress';
  import { onMount } from 'svelte';
  import { attempt_set, questions, questions_set } from '../../../stores';

  export let details;

  enum Stages {
    Permission = 'Testing video and audio...',
    InitialDetails = 'Initial details',
    Thinking = 'Time to think',
    Recording = 'Cameras rolling',
  }

  let stage = Stages.Permission;
  let loading = true;

  let thinking_duration;
  let answer_duration;
  let question;
  let description;

  let stream: MediaStream;
  let recorder: MediaRecorder;
  let video: HTMLVideoElement;

  let timer: number | null;

  let countdown = 5;

  onMount(async () => {
    const { data } = await httpService.get(
      `/questions/questions/${$page.params.id}`
    );
    details = data;
    thinking_duration = details?.thinking_duration;
    answer_duration = details?.answer_duration;
    question = details?.text;
    description = details?.description;
    loading = false;
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
      await httpService.post<{ id: number }>(
        `/video/attempt/${$page.params.id}/${$attempt_set}/`,
        form,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      if ($questions.length > 0) {
        location.assign(`/question/${$questions[0]}/record`);
      } else {
        await httpService.post(`/video/process/${$attempt_set}/`);
        goto(`/attempt-set/${$attempt_set}/stats`);
        $questions_set = null;
        $attempt_set = null;
        $questions = null;
      }
      NProgress.done();
    };
    recorder.stop();
    stream.getTracks().forEach((track) => track.stop());
    video.srcObject = undefined;
  };
</script>

{#if loading}
  <Loading withOverlay={false} class="m-auto" />
{:else}
  <div class="flex flex-col space-y-10 flex-1 items-center justify-center">
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
{/if}
