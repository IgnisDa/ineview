<script lang="ts">
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { Button, Loading } from 'carbon-components-svelte';
  import { onMount } from 'svelte';
  import { httpService } from '../../../lib/http';
  import { attempt_set, questions, questions_set } from '../../../stores';

  let details;
  let loading = true;

  $: $questions = details?.question_set?.map((s) => s.id);
  $: $questions_set = details?.id;

  const startInterview = async () => {
    const { data } = await httpService.post(`/video/attempt-set/`);
    console.log(data);
    $attempt_set = data.id;
    goto(`/question/${$questions[0]}/record`);
  };

  onMount(async () => {
    const { data } = await httpService.get(
      `/questions/questions-set/${$page.params.id}`
    );
    details = data;
    loading = false;
  });
</script>

{#if loading}
  <Loading withOverlay={false} class="m-auto" />
{:else}
  <div class="flex flex-col flex-1 w-full items-center justify-center">
    <div class="space-y-5 text-left">
      <div>
        <span>Created by:</span>
        <span class="text-2xl">
          {details?.user.username} ({details?.user.first_name}
          {details?.user.last_name})
        </span>
      </div>
      <div>
        <span>Created on:</span>
        <span class="text-2xl">
          {new Date(details?.created_date).toDateString()}
        </span>
      </div>
      <div>
        <span>Number of questions:</span>
        <span class="text-2xl">{details?.question_set.length}</span>
      </div>
      <div>
        <Button on:click={startInterview} kind="danger">Start interview</Button>
      </div>
    </div>
  </div>
{/if}
