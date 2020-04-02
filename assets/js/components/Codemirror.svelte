<script>
  import cm from "codemirror";
  import 'codemirror/lib/codemirror.css';
  import 'codemirror/mode/sql/sql.js';
  import 'codemirror/mode/python/python.js';
  import 'codemirror/mode/markdown/markdown.js';
  import 'codemirror/theme/idea.css'; 
  import key from "keymaster";
  import _ from "lodash"
  
  import { afterUpdate, onMount } from 'svelte'
  
  export let id, mode, on_change, text
  export let textarea, editor

  onMount(() => {
      editor = cm.fromTextArea(textarea, {
          mode: mode,
          theme: 'idea',
          lineNumbers: true,
          viewportMargin: Infinity
      });

      editor.on("change", on_change)
  })

  afterUpdate(() => {
    if (editor) editor.setOption('mode', mode)
  })
</script>

<style>
    #root {
        height: auto;
    }

    textarea {
      height: auto;
    }
</style>

<div id="root">
    <textarea bind:this={textarea}>{text}</textarea>
</div>
