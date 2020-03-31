<script>
  import cm from "codemirror";
  import './codemirror.css';
  import 'codemirror/lib/codemirror.css';
  import 'codemirror/mode/sql/sql.js';
  import 'codemirror/mode/python/python.js';
  import 'codemirror/theme/idea.css'; 
  import key from "keymaster";
  import _ from "lodash"
  
  import { onMount } from 'svelte'
  
  export let id, mode, on_change, text
  export let textarea, editor

  onMount(() => {
    console.log('initialize with ', text)
      editor = cm.fromTextArea(textarea, {
          mode: mode,
          theme: 'idea',
          lineNumbers: false
      });

      editor.on("change", on_change)
  });
</script>

<style>
    #root {
        height: auto;
        border: 1px solid black;
    }
</style>

<div id="root">
    <textarea bind:this={textarea}>{text}</textarea>
</div>
