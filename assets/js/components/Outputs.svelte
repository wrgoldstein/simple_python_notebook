<script>
  import Prism from "prismjs"
  import Chart from "svelte-charts"
  import "prismjs/components/prism-python"
  import "prismjs/themes/prism.css";
  import "katex";
  import AnsiUp from "ansi_up";
  import Slider from "./dynamic/Slider.svelte";
  import _ from "lodash";
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();
  
  const kinds = {
    Slider
  }

  export let outputs, channel

  const ansiup = new AnsiUp();

  outputs = outputs || [];

  function parse_svelte_props(output){
    const json = output.content.data['application/json']
    if (!json.kind) return ''
    return {

    }
  }

  function forward(event){
    dispatch("update", event.detail)
  }

  const state = {}

</script>

<style>
.table {
  max-width: 100%;
  overflow: scroll;
}

.chart {
  height: 15em;
  width: 90%;
  margin: auto;
}

.stdout {
  font-family: roboto;
}
</style>
{#each outputs as output}
  {#if output.msg_type == 'execute_result'}
    {#if "application/json" in output.content.data}
      <svelte:component
        on:update={forward}
        this={kinds[output.content.data['application/json'].kind]}
        {...output.content.data['application/json'].data}
      />
    {:else}
      <pre>{output.content.data['text/plain']}</pre>
    {/if}
  {:else if output.msg_type == 'stream'}
    <pre class="stdout">{output.content.text}</pre>
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
      {#if payload.data}
        <pre>
          {@html ansiup.ansi_to_html(payload.data['text/plain'])}
        </pre>
      {:else}
        <!-- {keepkernel: 0, source: "ask_exit"} means kernel dead -->
        kernel dead ?{JSON.stringify(payload)}
      {/if}
    {/each}
  {/if}
{/each}
