import Prism from "prismjs"
import "prismjs/components/prism-python"
import marked from "marked"
import katex from "katex"

marked.setOptions({
  highlight: function(code, language) {
    switch (language) {
      case 'python':
        return Prism.highlight(code, Prism.languages.python, 'python')
      default:
        return code
    }
  }
})

window.Prism = Prism
window.marked = marked
window.katex = katex

function trim_latex(source){
  return source.replace(/(^(\$|\n)*)|((\$|\n)*$)/g, '')
}

var matches, output = [];


function parse_math(s){
  let lines = s.split('\n')
  lines.push('\n') // hack to make sure trailing $$ are picked up
  let parsed = []
  let match, flag, display
  let line = lines.shift()
  let line_re = /(?<!\\)\$(.*)(?<!\\)\$/
  while (lines.length){
    
    if (line.trim() == '$$'){
      if (flag){
        // close display mode
        flag = false
        parsed.push(
          katex.renderToString(display.join('\n'),
            { displayMode: true }
          )
        )
      } else {
        flag = true
        display = []
      }
    }
    else if (flag){
      // add to display
      display.push(line)
    }
    else if (match = line.match(line_re)){
      line = line.replace(line_re, (_a,m,_b)=>{
        return katex.renderToString(m)
      })
      parsed.push(line)
    }
    else {
      parsed.push(line)
    }
    line = lines.shift()
  }
  return parsed.join('\n')
}



export function mark(source){
  return marked(parse_math(source))
}
