<script>
  import AnsiUp from "ansi_up";
  export let outputs

  const ansiup = new AnsiUp();

  outputs = outputs || [];


</script>

<style>
.table {
  max-width: 100%;
  overflow: scroll;
}
</style>

{#each outputs as output}
  {#if output.msg_type == 'execute_result'}
    <pre>{output.content.data['text/plain']}</pre>
  {:else if output.msg_type == 'stream'}
    <pre>{output.content.text}</pre>
  {:else if output.msg_type == 'display_data'}
    {#if 'image/png' in output.content.data}
      <!-- svelte-ignore a11y-missing-attribute -->
      <img src="data:image/png;base64,{output.content.data['image/png']}" />
    {:else if 'text/html' in output.content.data}
      <div class="table">
        {@html output.content.data['text/html']}
      </div>
    {/if}
  {:else if output.msg_type == 'error'}
    <pre>
      {@html ansiup.ansi_to_html(output.content.traceback.join('\n'))}
    </pre>
  {:else if output.msg_type == 'execute_reply'}
    {#each output.content.payload || [] as payload}
      <pre>
        {@html ansiup.ansi_to_html(payload.data['text/plain'])}
      </pre>
    {/each}
  {/if}
{/each}
