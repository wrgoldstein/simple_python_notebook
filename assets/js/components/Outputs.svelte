<script>
  import Prism from "prismjs"
  import "prismjs/components/prism-python"
  import "prismjs/themes/prism.css";
  import "katex";
  import AnsiUp from "ansi_up";
  export let outputs

  const ansiup = new AnsiUp();

  outputs = outputs || [];

  function handleRichOutput(html){
    /*
      This is a hack to handle arbitrary 
      html and javascript plots. 
      
      (!) It's unsafe.
    */
    const re = /((.|\n*)+)<script.*>((.|\n*)+)<\/script>/
    const match = html.match(re)
    if (!match) return html
    const html_ = match[1]
    const script = match[3]
    setTimeout(() => eval(script), 20)
    return html_
  }
</script>

<style>
.table {
  max-width: 100%;
  overflow: scroll;
}
</style>

{#each outputs as output}
  {#if output.msg_type == 'execute_result'}
    {#if "text/plain" in output.content.data}
      { @html handleRichOutput(output.content.data['text/html']) }
    {:else}
      <pre>{output.content.data['text/plain']}</pre>
    {/if}
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
