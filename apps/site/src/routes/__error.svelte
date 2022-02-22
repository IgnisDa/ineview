<script context="module">
  export function load({ error, status }) {
    return {
      props: {
        title: `${status}: ${error.message}`,
      },
    };
  }
</script>

<script>
  export let title;
</script>

<div class="text-white text-center">
  <h1 class="text-2xl">{title}</h1>
</div>
