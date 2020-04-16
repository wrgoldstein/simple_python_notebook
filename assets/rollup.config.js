import resolve from 'rollup-plugin-node-resolve';
import svelte from 'rollup-plugin-svelte';
import commonjs from 'rollup-plugin-commonjs';
import css from 'rollup-plugin-css-only'

const onwarn = warning => {
  if (warning.code === 'CIRCULAR_DEPENDENCY' && /moment/.test(warning.importer)) {
    return
  } else if (warning.code === 'CIRCULAR_DEPENDENCY' && /d3/.test(warning.importer)) {
    return
  }
  console.warn(`(!) ${warning.message}`)
}

module.exports = {
    input: ['js/app.js', 'js/index.js', 'css/global.css'],
    output: {
      dir: '../priv/static/js',
      sourcemap: true,
      format: 'es'
    },
  onwarn,
  plugins: [
    resolve({
      mainFields: ['module', 'main'],
      customResolveOptions: {
        moduleDirectory: [
          "deps/phoenix/priv/static",
          "deps/phoenix_html/priv/static"
        ]
      }
    }),
    svelte({
      css:  function(css){
        css.write('../priv/static/css/svelte.css')
      }
    }),
    resolve({
      mainFields: ['module', 'main']
    }),
    css({exclude: "**/global.css", output: '../priv/static/css/app.css'}),
    css({include: "**/global.css", output: '../priv/static/css/global.css'}),
    commonjs({
      // search for files other than .js files (must already
      // be transpiled by a previous plugin!)
      extensions: [ '.js', '.html' ],  // Default: [ '.js' ]
    })
  ]
};
