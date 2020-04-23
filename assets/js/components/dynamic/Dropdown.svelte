<script>
	import { createEventDispatcher, onMount } from 'svelte';

	const dispatch = createEventDispatcher();

  export let id, options, value

  const updateComponent = () => {
    dispatch('updateComponent', {
      updated_id: id,
      updated_value: `'${value}'` // value must be quoted
    })
  }

  onMount(updateComponent)
  $: updateComponent()
</script>

<div class="main">
  <select bind:value={value} on:change={updateComponent}>
    {#each options as option}
      <option value={option}>{option}</option>
    {/each}
  </select>
</div>
<slot>
</slot>

<style>
.main {
  width: 100%;
}

select {
  width: 80%;
}
</style>