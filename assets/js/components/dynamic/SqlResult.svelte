<script>
  export let name, status, nrows, seconds, errormsg
</script>

<div class="main">
{#if status == "OK"}
  
  Fetched {nrows} rows 
  in {seconds.toFixed(3)} seconds. 

  Saved as <span class="name">{name}</span>.
{:else}
  <pre>
    {errormsg}
  </pre>
{/if}
</div>

<style>
.main {
  font-size: .8em;
  font-family: Fira Code;
}

.name {
  background-color: #eee;
  padding: 3px;
  border-radius: 2px;
}
</style>