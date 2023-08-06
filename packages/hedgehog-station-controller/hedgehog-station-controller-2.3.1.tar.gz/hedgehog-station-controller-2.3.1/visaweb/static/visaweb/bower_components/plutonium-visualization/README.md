# Plutonium Visualization 

[![Build Status](https://travis-ci.org/lordoftheflies/plutonium-chart-widget.svg?branch=master)](https://travis-ci.org/lordoftheflies/plutonium-visualization)
[![Published on webcomponents.org](https://img.shields.io/badge/webcomponents.org-published-blue.svg)](https://www.webcomponents.org/element/lordoftheflies/plutonium-visualization)

Visualization library for integrate Polymer with D3 and add SVG support.

## Install

```bash
$ bower install lordoftheflies/plutonium-visualization --save
```

## Import

```html
<link rel="import" href="/bower_components/lordoftheflies/plutonium-visualization.html">
```

## Usage

<!---
```
<custom-element-demo height="368">
  <template>
    <script src="../webcomponentsjs/webcomponents-lite.min.js"></script>
    <link rel="import" href="app-drawer/app-drawer.html">
    <link rel="import" href="app-header/app-header.html">
    <link rel="import" href="app-toolbar/app-toolbar.html">
    <link rel="import" href="demo/sample-content.html">
    <link rel="import" href="../iron-icons/iron-icons.html">
    <link rel="import" href="../paper-icon-button/paper-icon-button.html">
    <link rel="import" href="../paper-progress/paper-progress.html">
    <style is="custom-style">
      html, body {
        margin: 0;
        font-family: 'Roboto', 'Noto', sans-serif;
        -webkit-font-smoothing: antialiased;
        background: #f1f1f1;
        max-height: 368px;
      }
      app-toolbar {
        background-color: #4285f4;
        color: #fff;
      }

      paper-icon-button {
        --paper-icon-button-ink-color: white;
      }

      paper-icon-button + [main-title] {
        margin-left: 24px;
      }
      paper-progress {
        display: block;
        width: 100%;
        --paper-progress-active-color: rgba(255, 255, 255, 0.5);
        --paper-progress-container-color: transparent;
      }
      app-header {
        @apply(--layout-fixed-top);
        color: #fff;
        --app-header-background-rear-layer: {
          background-color: #ef6c00;
        };
      }
      app-drawer {
        --app-drawer-scrim-background: rgba(0, 0, 100, 0.8);
        --app-drawer-content-container: {
          background-color: #B0BEC5;
        }
      }
      sample-content {
        padding-top: 64px;
      }
    </style>
    <next-code-block></next-code-block>
  </template>
</custom-element-demo>
```
-->

```html
<app-header reveals>
  <app-toolbar>
    <paper-icon-button icon="menu" onclick="drawer.toggle()"></paper-icon-button>
    <div main-title>My app</div>
    <paper-icon-button icon="delete"></paper-icon-button>
    <paper-icon-button icon="search"></paper-icon-button>
    <paper-icon-button icon="close"></paper-icon-button>
    <paper-progress value="10" indeterminate bottom-item></paper-progress>
  </app-toolbar>
</app-header>
<app-drawer id="drawer" swipe-open></app-drawer>
<sample-content size="10"></sample-content>
```


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

### Prepare for development

#### Install the Polymer-CLI

First, make sure you have the [Polymer CLI](https://www.npmjs.com/package/polymer-cli) installed. Then run `polymer serve` to serve your application locally.

#### Viewing Your Application

```
$ polymer serve
```

#### Building Your Application

```
$ polymer build
```

This will create a `build/` folder with `bundled/` and `unbundled/` sub-folders
containing a bundled (Vulcanized) and unbundled builds, both run through HTML,
CSS, and JS optimizers.

You can serve the built versions by giving `polymer serve` a folder to serve
from:

```
$ polymer serve build/bundled
```

#### Running Tests

```
$ polymer test
```

Your application is already set up to be tested via [web-component-tester](https://github.com/Polymer/web-component-tester). Run `polymer test` to run your application's test suite locally.

## History

TODO: Write history

## Credits

TODO: Write credits

## License

TODO: Write license