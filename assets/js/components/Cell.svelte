<script>
  import Codemirror from "./Codemirror.svelte";
  import Outputs from "./Outputs.svelte"
  import { cells } from "../stores";
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

  let cm
  let flavor = 'markdown'
  let text = $cells.get(uuid).text;
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

  .view {
    display: none;
  }

  .flavor {
    color: grey;
  }

  .active {
    color: black;
  }
</style>

<div>
  <div>
    <div style='display: flex; font-family: monospace;'>
      <button class:flavor class:active={flavor == 'python'} on:click={() => flavor = 'python'}>python</button>
      <button class:flavor class:active={flavor == 'markdown'} on:click={() => flavor = 'markdown'}>markdown</button>
    </div>
    <div class:view={mode == 'view'}>
      <Codemirror bind:editor={cm} {text} mode={flavor} {on_change} />
    </div>
    <button on:click={remove_me}>✕</button>
    <button on:click={send_text}>Send me</button>
    <Outputs {outputs} />
  </div>
</div>
