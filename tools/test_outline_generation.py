#!/usr/bin/env python3
"""Regression: runtime class names must never create a second authored outline."""
import re
from sync_navigation import add_outline,root
main='<main><section><h2 id="one">One</h2></section><section><h2 id="two">Two</h2></section></main>'
for attr in ['class="page-outline is-enhanced"','aria-label="On this page" class="is-enhanced page-outline"',"class='is-enhanced page-outline is-in-reading-area'"]:
 authored='<nav '+attr+'><ol><li><a href="#one">One</a></li><li><a href="#two">Two</a></li></ol></nav>'
 generated='<nav class="page-outline" data-page-outline="generated"><ol><li>Duplicate</li></ol></nav>'
 text=authored+generated+main
 for _ in range(3):text=add_outline(root/'pricing/index.html',text)
 assert text==authored+main,'Preserve exactly one authored outline, regardless of class order'
text=main
for _ in range(3):text=add_outline(root/'pricing/index.html',text)
assert text.count('class="page-outline"')==1
assert text.count('id="page-outline-select"')==1
print('Outline generation is idempotent with enhanced, reordered and single-quoted class attributes.')
