<script>
	export let name;

	let text = "Write some python here"
	let output

	function sendText(){
		fetch('/python', {
            method: 'POST',
            headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'x-csrf-token': window.csrfToken
			},
            body: JSON.stringify({ command: text })
        })
        .then(resp => resp.json())
        .then(s => {
			console.log(s)
			output = s.stdout || s.stderr
		})
	}
</script>

<style>
	h1 {
		color: black;
	}

	textarea {
		width: 50vw;
		height: 25vh;
	}
</style>

<h1>Hello {name}!</h1>

<textarea bind:value={text}></textarea>
<textarea bind:value={output}></textarea>

<button on:click={sendText}>Send me </button>
