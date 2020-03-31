<script>
  import { onMount } from 'svelte'
  import phx from "phoenix";
  import Cell from "./Cell.svelte"
  import { socket, cells } from "./stores"


  let channel, client_id

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
    cells.set($cells.set(uuid, { text: '' , uuid }))
  }

  /*
    Need to be able to
      - Set state for the first time when logging in
        * Get each cell and its text
      - Update state for all subscribers on keystroke
      - Show where cursor is for each subscriber...
  */

  onMount(() => {
    socket.set(new phx.Socket("/socket", {params: {token: '123'}}))
    $socket.connect()

    // Now that you are connected, you can join channels with a topic:
    channel = $socket.channel("room:boom", {})
    channel.join()
      .receive("ok", resp => { 
        client_id = resp.client_id
        if (resp.state.length == 0) {
          add_cell()
        } else {
          resp.state.forEach(cell => {
            cells.set($cells.set(cell.uuid, cell))
          })
        }
        console.log("Joined successfully", resp) 
      })
      .receive("error", resp => { console.log("Unable to join", resp) })
  })
  export let name;
</script>

<style>
	h1 {
		color: black;
	}
</style>

<h1>Hello {name}!</h1>
{#each Array.from($cells.values()) as cell, i (cell.uuid) }
  <Cell {client_id} uuid={cell.uuid} {channel}/>
{/each}

<button on:click={add_cell}>Add cell</button>
