
import { writable, readable, derived } from 'svelte/store'

export const cells = writable(new Map())
export const socket = writable()
