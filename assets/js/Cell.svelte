<script>
  import Codemirror from "./codemirror/Codemirror.svelte";
  import AnsiUp from "ansi_up";
  import { cells } from "./stores"
  import _ from "lodash"

  export let uuid, channel, client_id
  let cm
  let text = $cells.get(uuid).text

  const ansiup = new AnsiUp();

  let stdout, stderr, payload;

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
        stdout = s.stdout; //.replace(new RegExp('\n', 'g'), '')
        stderr = s.stderr;
        payload = s.payload;
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
  .stdout {
    font-family: mono;
  }
</style>

<div>
  <div>
    <Codemirror bind:editor={cm} {text} mode="python" {on_change} />
    {#if stdout}
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
    {/if}
  </div>
  <button on:click={sendText}>Send me</button>
</div>
