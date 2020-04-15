<script>
  import Codemirror from "./Codemirror.svelte";
  import Outputs from "./Outputs.svelte"
  import { mark } from "../helpers.mjs"
  import { cells } from "../stores";
  import _ from "lodash";
  export let i, uuid, channel, client_id, outputs, mode, flavor
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
    One of ['python', 'markdown', 'sql']

  text: string
    The content of the cell
  */

  let cm
  let text = $cells.get(uuid).text;
  let last_update
  let dynamic_outputs = {}

  function me(){
    return { i, uuid, text, client_id, outputs, flavor }
  }
  
  function flavorize(language){
    return () => {
      flavor = language
      channel.push("update", me());
    }
  }

  function for_me(resp) {
    const from_me = resp.client_id == client_id;
    const for_this_cell = resp.uuid == uuid;
    return !from_me && for_this_cell;
  }

  channel.on("update", resp => {
    if (for_me(resp)) {
      text = last_update = resp.text;
      flavor = resp.flavor
      cm.setValue(text);
    }
  });

  channel.on("results", resp => {
    if (resp.uuid == uuid) {
      outputs = resp.outputs;
    }
  });

    channel.on("dynamic_outputs", resp => {
      dynamic_outputs[resp.id] = resp.result;
    });

  function send_text() {
    if ( flavor == 'markdown'){
      outputs = [{
        msg_type: 'display_data',
        content: {
          data: {
            'text/html': mark(text)
          }
        }
      }]
      channel.push("results", me())
    } else {
      channel.push("execute", me());
    }
  }

  function remove_me() {
    channel.push("remove", { i, uuid, client_id });
  }

  const on_change = _.debounce((cm) => {
    text = cm.getValue();
    if (last_update == text) return;
    channel.push("update", { ...me(), text });
  }, 100);

  const propagate_updates = _.debounce((event) =>{
    const { updated_id, updated_value } = event.detail
    channel.push("dynamics", {
      ...me(),
      updated_id,
      updated_value
    })
  }, 100)
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
    {#if mode == 'edit'}
      <div style='display: flex; font-family: monospace;'>
        <button class:flavor class:active={flavor == 'python'} on:click={flavorize('python')}>python</button>
        <button class:flavor class:active={flavor == 'markdown'} on:click={flavorize('markdown')}>markdown</button>
        <button class:flavor class:active={flavor == 'markdown'} on:click={flavorize('sql')}>sql</button>
      </div>
    {/if}
    <div class:view={mode == 'view'}>
      <Codemirror on:submit={send_text} bind:editor={cm} {text} mode={flavor} {on_change} />
    </div>
    {#if mode == 'edit'}
      <button on:click={remove_me}>✕</button>
      <button on:click={send_text}>Send me</button>
    {/if}
    <Outputs
      on:updateComponent={propagate_updates}
      {outputs}
      {dynamic_outputs}
      {channel}/>
  </div>
</div>
