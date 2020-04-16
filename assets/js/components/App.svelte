<script>
  import { onMount } from 'svelte'
  import phx from "phoenix";
  import Cell from "./Cell.svelte"
  import { socket, cells } from "../stores"


  let channel, client_id
  let mode = "edit"
  let alive = false

  function generateUID() {
    // I generate the UID from two parts here 
    // to ensure the random number provide enough bits.
    var firstPart = (Math.random() * 46656) | 0;
    var secondPart = (Math.random() * 46656) | 0;
    firstPart = ("000" + firstPart.toString(36)).slice(-3);
    secondPart = ("000" + secondPart.toString(36)).slice(-3);
    return firstPart + secondPart;
  }

  function add_cell(){
    const uuid = generateUID()
    const i = $cells.size
    const cell = { i, uuid, text: '', outputs: [], flavor: 'python' }
    channel.push("add", cell)
  }

  function set_cells(state){
    state.forEach(cell => {
      cells.set($cells.set(cell.uuid, cell))
    })
  }

  function update_state(resp){
    alive = true
    client_id = resp.client_id;
    (resp.state.length == 0) ? add_cell() : set_cells(resp.state)
  }

  function restart_kernel(resp){
    alive = false
    channel.push("restart")
  }

  onMount(() => {
    socket.set(new phx.Socket("/socket", {params: {token: '123'}}))
    $socket.connect()

    // Now that you are connected, you can join channels with a topic:
    channel = $socket.channel("room:boom", {})
    channel.join()
      .receive("ok", update_state)
      .receive("error", resp => { console.log("Unable to join", resp) })

    channel.on("add", resp => {
      cells.set($cells.set(resp.uuid, resp))
    })

    channel.on("remove", resp => {
      const temp = $cells
      temp.delete(resp.uuid)
      cells.set(temp)
    })

    channel.on("started", resp => {
      alive = true
    })
  })
  export let name;
</script>

<style>
#header {
  font-family: 'Comic Neue';
  font-size: 16px;
  color: grey;
  border-bottom: 1px solid lightgrey;
}

.mode-button {
  align-self: center;
  height: 3em;
  min-width: 8em;
}

.dot {
  height: 25px;
  width: 25px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
  vertical-align: middle;
}

.alive {
  background-color: #afa;
}

.right {
  float: right;
}

.wide {
  min-width: 10em;
}

spacer {
  width: 1em;
}

main {
  width: 60%;
  min-width: 600px;
  margin: auto;
}
</style>


<p id="header">Shared session python notebook demo</p>
<div style='font-family: monospace;'>
  <span>mode: { mode }</span>
  <spacer />
  <button class="mode-button" on:click={() => mode = 'edit'}>edit</button>
  <button class="mode-button" on:click={() => mode = 'view'}>view</button>
  <spacer />
  <button disabled class="mode-button right wide" on:click={() => console.log('run')}>run all</button>
  <button class="mode-button right wide" on:click={restart_kernel}>restart kernel</button>
  <span class:alive class="dot"></span>
</div>
<main>
  {#each Array.from($cells.values()) as cell, i (cell.uuid) }
    <Cell {i}
          {client_id}
          uuid={cell.uuid}
          outputs={cell.outputs}
          {channel}
          {mode}
          flavor={cell.flavor}
    />
  {/each}

  {#if mode == 'edit'}
    <button on:click={add_cell}>Add cell</button>
  {/if}
</main>