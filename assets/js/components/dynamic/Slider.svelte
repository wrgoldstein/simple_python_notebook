<script>
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

  export let varname, min, max, value
  let value_ = value

  /*
  value not updating when slider moves..
  Try exporting value and using another
  variable internally?
  */

  function on_change(event){
    dispatch('update', {
      varname,
      value: event.target.value
    })
  }
</script>

<input bind:value={value_} on:input={on_change} type="range" {min} {max} />
