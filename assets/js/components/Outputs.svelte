<script>
  import Prism from "prismjs"
  import Chart from "svelte-charts"
  import "prismjs/components/prism-python"
  import "prismjs/themes/prism.css";
  import "katex";
  import AnsiUp from "ansi_up";
  import Slider from "./dynamic/Slider.svelte";
  import Dropdown from "./dynamic/Dropdown.svelte";
  import _ from "lodash";
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();
  
  const kinds = {
    Slider,
    Dropdown,
    Chart
  }

  export let outputs, channel;
  export let dynamic_outputs = {};

  const ansiup = new AnsiUp();

  outputs = outputs || [];

  function parse_svelte_props(output){
    const json = output.content.data['application/json']
    if (!json.kind) return ''
    return {

    }
  }

  function forward(event){
    dispatch("updateComponent", event.detail)
  }

  const isSpl = (output) => {
    return !!(
      output.content &&
      output.content.data &&
      output.content.data["application/json"] &&
      output.content.data['application/json'].spl)
  }

  const state = {}
</script>

<style>
.table {
  max-width: 100%;
  overflow: scroll;
}

.stdout {
  font-family: roboto;
}
</style>
{#each outputs as output}
  { #if isSpl(output) }
    { console.log(output)}
    <svelte:component
      on:updateComponent={forward}
      this={kinds[output.content.data['application/json'].kind]}
      {...output.content.data['application/json'].data}
    >
    {#if dynamic_outputs[output.content.data['application/json'].data.id]}
      <svelte:self
        outputs={dynamic_outputs[output.content.data['application/json'].data.id]}
      />
    {/if}
    </svelte:component>
  {:else if output.msg_type == 'execute_result'}
    <pre>{output.content.data['text/plain']}</pre>
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
