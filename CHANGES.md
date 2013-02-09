CHANGES
=======

## Development

## Version 0.3.1 (2013-02-09T09:41:19Z)

 * add `register_directives` and `register_roles` options of rst handler
 * remove all existing directives and roles of rst handler

## Version 0.3 (2013-02-06T11:31:43Z)

 * fix `update_source` cannot handle unicode and utf8 enocded str by ensuring everything is utf8 encoded internally
 * add Text handler for plain text
 * add HTML handler

## Version 0.2 (2013-02-02T12:02:10Z)

 * Fix trailing newlines becoming spaces in title
 * fix empty label '' in labels array
 * Add handler options `markup_prefix` and `markup_suffix`
 * Add header and handler option `id_affix` to avoid HTML element ID conflict across posts
 * Add handler for AsciiDoc

## Version 0.1.2 (2013-01-18T05:47:16Z)

 * Fix handler rst `settings_overrides` not getting updates

## Version 0.1.1 (2013-01-17T20:29:46Z)

 * Fix handlers not getting update of options

## Version 0.1 (2013-01-17T05:22:54Z)

 * First versioned release
