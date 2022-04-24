<script lang="ts">
  import { Loading } from 'carbon-components-svelte';
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { httpService } from '$lib/http';
  import PieChart from 'svelte-chartjs/src/Pie.svelte';
  import randomColor from 'randomcolor';

  const emotions = [
    'angry',
    'disgust',
    'fear',
    'happy',
    'neutral',
    'sad',
    'surprise',
  ];

  let chartData = [];
  let loading = true;

  onMount(async () => {
    const { data } = await httpService.get(
      `/video/attempt-set/${$page.params.id}`
    );
    loading = false;
    const attemptsData = {};
    for (const attempt of data.attempt_set) {
      const emotional = {
        angry: 0,
        disgust: 0,
        fear: 0,
        happy: 0,
        neutral: 0,
        sad: 0,
        surprise: 0,
      };
      for (const frame of attempt.data) {
        const emotions = frame[0].emotions;
        emotional['angry'] += emotions.angry || 0;
        emotional['disgust'] += emotions.disgust || 0;
        emotional['fear'] += emotions.fear || 0;
        emotional['happy'] += emotions.happy || 0;
        emotional['neutral'] += emotions.neutral || 0;
        emotional['sad'] += emotions.sad || 0;
        emotional['surprise'] += emotions.surprise || 0;
      }
      attemptsData[`attempt-${attempt.id}`] = attempt.data;
      const chart = {
        labels: Object.values(emotions),
        datasets: [
          {
            label: `For video ${attempt.id}`,
            data: Object.values(emotional),
            backgroundColor: [...Array(5)].map((_) => randomColor()),
            hoverOffset: 4,
          },
        ],
      };
      chartData.push(chart);
    }
  });
</script>

{#if loading}
  <Loading withOverlay={false} class="m-auto" />
{:else}
  <div class="h-full w-full grid py-10 grid-cols-2 justify-items-center">
    {#each chartData as chart}
      <div class="h-[400px] w-[400px]">
        <PieChart data={chart} />
      </div>
    {/each}
  </div>
{/if}
