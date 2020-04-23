<script>
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

  export let id, options, value

  /*
  value not updating when slider moves..
  Try exporting value and using another
  variable internally?
  */

  function on_change(event){
    dispatch('updateComponent', {
      updated_id: id,
      updated_value: event.target.value
    })
  }
</script>

<div class="main">
  <select>
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

input {
  width: 80%;
}
</style>