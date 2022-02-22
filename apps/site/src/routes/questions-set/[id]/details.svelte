<script context="module">
  import { goto } from '$app/navigation';
  import { httpService } from '$lib/http';
  import { questions, questions_set } from '../../../stores';

  /** @type {import('@sveltejs/kit').Load} */
  export async function load({ params }) {
    try {
      const { data } = await httpService.get(
        `/questions/questions-set/${params.id}`
      );
      return { props: { details: data } };
    } catch {
      return { error: 'This question set does not exist', status: 404 };
    }
  }
</script>

<script lang="ts">
  export let details;

  $questions = details.question_set.map((s) => s.id);
  $questions_set = details.id;

  const startInterview = () => goto(`/question/${$questions[0]}/record`);
</script>

<div class="flex flex-col flex-1 text-white w-full items-center justify-center">
  <div class="space-y-5 text-left">
    <div>
      <span>Created by:</span>
      <span class="text-2xl">
        {details.user.username} ({details.user.first_name}
        {details.user.last_name})
      </span>
    </div>
    <div>
      <span>Created on:</span>
      <span class="text-2xl">
        {new Date(details.created_date).toDateString()}
      </span>
    </div>
    <div>
      <span>Number of questions:</span>
      <span class="text-2xl">{details.question_set.length}</span>
    </div>
    <div>
      <button
        on:click={startInterview}
        class="rounded-lg bg-indigo-700 py-2 px-3 text-2xl"
      >
        Start interview
      </button>
    </div>
  </div>
</div>
