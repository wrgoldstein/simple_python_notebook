<script>
	import { createEventDispatcher, onMount } from 'svelte';

	const dispatch = createEventDispatcher();

  export let id, min, max, value

  onMount(() => {
    dispatch('updateComponent', {
      updated_id: id,
      updated_value: value
    })
  })

  $: {

    dispatch('updateComponent', {
      updated_id: id,
      updated_value: value
    })
  }
</script>

<div class="main">
  <label>{min}</label>
  <input bind:value={value} type="range" {min} {max} />
  <label>{max}</label>
</div>
<slot>
</slot>

<style>
.main {
  width: 100%;
}

input {
  width: 80%;
}
</style>