<script>
  import Codemirror from "./codemirror/Codemirror.svelte";
  import AnsiUp from "ansi_up";
  import { cells } from "./stores";
  import _ from "lodash";

  export let i, uuid, channel, client_id, outputs, mode;
  /*
  Cell component for individual python REPL

  Props
  ----------
  i: integer
    The position of this cell

  uuid: string
    The unique identifier of this cell

  channel: phoenix.Socket.channel
    The room (notebook) this session is in

  client_id: string
    The unique identifier of the client

  outputs: array[object]
    Outputs from executed code (from ipython kernel)

    This is only provided as a prop when loading
    initial state

  mode: string
    One of ['view', 'edit']


  Variables
  ----------
  flavor: string
    One of ['python', 'markdown']

  text: string
    The content of the cell
  */

  let cm, flavor;
  let text = $cells.get(uuid).text;

  const ansiup = new AnsiUp();

  outputs = outputs || [];

  let last_update;

  function for_me(resp) {
    const from_me = resp.client_id == client_id;
    const for_this_cell = resp.uuid == uuid;
    return !from_me && for_this_cell;
  }

  channel.on("update", resp => {
    if (for_me(resp)) {
      text = last_update = resp.text;
      cm.setValue(text);
    }
  });

  channel.on("results", resp => {
    if (resp.uuid == uuid) {
      console.log(resp);
      outputs = resp.outputs;
    }
  });

  function send_text() {
    channel.push("execute", { i, uuid, text, client_id });
  }

  function remove_me() {
    channel.push("remove", { i, uuid, text, client_id });
  }

  function _on_change(cm) {
    text = cm.getValue();
    if (last_update == text) return;
    channel.push("update", { i, uuid, text, client_id });
  }
  const on_change = _.debounce(_on_change, 100);
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

  .view {
    display: none;
  }
</style>

<div>
  <div>
    <div class:view={mode == 'view'}>
      <Codemirror bind:editor={cm} {text} mode="python" {on_change} />
    </div>
    <button on:click={remove_me}>✕</button>
    <button on:click={send_text}>Send me</button>
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
  </div>
</div>
