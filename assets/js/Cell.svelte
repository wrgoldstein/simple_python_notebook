<script>
  import Codemirror from "./codemirror/Codemirror.svelte";
  import AnsiUp from "ansi_up";
  import { cells } from "./stores"
  import _ from "lodash"

  export let uuid, channel, client_id
  let cm
  let text = $cells.get(uuid).text

  const ansiup = new AnsiUp();

  let outputs = []
  let last_update

  channel.on("update", resp => {
    const from_me = resp.client_id == client_id
    const for_this_cell = resp.uuid == uuid
    if (!from_me && for_this_cell){
      text = last_update = resp.text
      cm.setValue(text)
    }
  })

  function sendText() {
    fetch("/python", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "x-csrf-token": window.csrfToken
      },
      body: JSON.stringify({ command: text })
    })
      .then(resp => resp.json())
      .then(s => {
        outputs = s
        console.log(outputs)
      });
  }

  function _on_change(cm) {
    text = cm.getValue();
    console.log({ uuid, text, client_id })
    if (last_update == text) return
    channel.push("update", { uuid, text, client_id })
  }
  const on_change = _.debounce(_on_change, 100)

</script>

<style>
  button {
    margin-top: 1em;
    float: right;
  }

  .table {
    max-width: 100%;
    overflow: scroll;
  }
</style>

<div>
  <div>
    <Codemirror bind:editor={cm} {text} mode="python" {on_change} />
    <button on:click={sendText}>Send me</button>
    {#each outputs as output }
      {#if output.msg_type == 'execute_result'}
        <pre>{output.content.data['text/plain']}</pre>
      {:else if output.msg_type == 'stream'}
        <pre>{output.content.text}</pre>
      {:else if output.msg_type == 'display_data'}
        {#if "image/png" in output.content.data }
          <!-- svelte-ignore a11y-missing-attribute -->
          <img src="data:image/png;base64,{output.content.data["image/png"]}">
        {:else if "text/html" in output.content.data }
          <div class="table">
            { @html output.content.data['text/html'] }
          </div>
        {/if}
      {:else if output.msg_type == 'error'}
        <pre>
          { @html ansiup.ansi_to_html(output.content.traceback.join("\n")) }
        </pre>
      {:else if output.msg_type == 'execute_reply'}
        {#each output.content.payload as payload }
          <pre>
            {@html ansiup.ansi_to_html(payload.data['text/plain'])}
          </pre>
        {/each}
      {/if}
    {/each }
    <!-- {#if stdout}
      <div class="stdout">
        {@html stdout}
      </div>
    {/if}
    {#if stderr}
      <div class="stderr">
        {@html stderr}
      </div>
    {/if}
    {#if payload}
      <div class="payload">
        {#each payload as load}
          <pre>
            {@html ansiup.ansi_to_html(load)}
          </pre>
        {/each}
      </div>
    {/if} -->
  </div>
</div>
