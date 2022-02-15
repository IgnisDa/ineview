<script lang="ts">
  import RecordIcon from 'svelte-icons/ti/TiMediaRecord.svelte';

  export let isDisabled: boolean;
  export let timer: number;
</script>

<div class="space-y-3">
  <span
    class="flex font-semibold font-mono text-white text-3xl items-center justify-center"
  >
    {timer}
  </span>
  <button
    disabled={isDisabled}
    class={`rounded-lg bg-warm-gray-800 h-12 text-red-600 transition-transform hover:scale-110 flex items-center pr-2 ${
      isDisabled && 'animate-bg'
    }`}
    on:click
  >
    <RecordIcon title="Record" />
    <span
      class="flex font-serif font-semibold text-green-500 uppercase items-center justify-center"
    >
      Record
    </span>
  </button>
</div>

<style lang="scss">
  $base-color: rgba(220, 38, 38);
  $base-color-pulsed: rgba(127, 29, 29);

  .animate-bg {
    color: $base-color;
    animation-name: pulse-color;
    animation-duration: 1.5s;
    animation-iteration-count: infinite;
  }

  @keyframes pulse-color {
    0% {
      color: $base-color;
    }
    50% {
      color: $base-color-pulsed;
    }
    100% {
      color: $base-color;
    }
  }
</style>
