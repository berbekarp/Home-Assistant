# 🍄 Mushroom

[![hacs][hacs-badge]][hacs-url]
[![release][release-badge]][release-url]
![downloads][downloads-badge]
![build][build-badge]
[![translations][translations-badge]][weblate-url]

<a href="https://www.buymeacoffee.com/piitaya" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/white_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

![Overview](https://user-images.githubusercontent.com/5878303/152332130-760cf616-5c40-4825-a482-bb8f1f0f5251.png)

## What is mushroom ?

Mushroom is a collection of cards for [Home Assistant][home-assistant] Dashboard UI.

Mushroom mission is to propose easy to use components to build your [Home Assistant][home-assistant] dashboard.

### Features

- 🛠 Editor for **all cards** and and **all options** (no need to edit `yaml`)
- 😍 Icon picker
- 🖌 Color picker
- 🚀 0 dependencies : no need to install another card.
- 🌈 Based on Material UI colors
- 🌓 Light and dark theme support
- 🎨 Optional theme customization
- 🌎 Internationalization


### Cards

Different cards are available for differents entities :

- 🚨 [Alarm card](docs/cards/alarm-control-panel.md)
- 🔔 [Chips card](docs/cards/chips.md)
- 🌡 [Climate card](docs/cards/climate.md)
- 🪟 [Cover card](docs/cards/cover.md)
- 🪄 [Entity card](docs/cards/entity.md)
- 🕳 [Empty card](docs/cards/empty.md)
- 💨 [Fan card](docs/cards/fan.md)
- 💧 [Humidifier card](docs/cards/humidifier.md)
- 💡 [Light card](docs/cards/light.md)
- 🔒 [Lock card](docs/cards/lock.md)
- 📺 [Media card](docs/cards/media-player.md)
- 🔢 [Number card](docs/cards/number.md)
- 🙋 [Person card](docs/cards/person.md)
- 📑 [Select card](docs/cards/select.md)
- 🛠 [Template card](docs/cards/template.md)
- ✏️ [Title card](docs/cards/title.md)
- 📦 [Update card](docs/cards/update.md)
- 🧹 [Vacuum card](docs/cards/vacuum.md)

### Legacy cards

Some cards are considered as legacy, are not available in the card picker but you can still use them :

- 🛠 [Legacy Template card](docs/cards/legacy-template.md)

### Badges

A [template badge](docs/badges/template.md) is available if you're using at least Home Assistant 2024.8.

### Theme customization

Mushroom works without theme but you can add a theme for better experience by installing the [Mushroom Themes](https://github.com/piitaya/lovelace-mushroom-themes). If you want more information about themes, check out the official [Home Assistant documentation about themes][home-assitant-theme-docs].

## Development server

### Home assistant demo

You can run a demo instance of Home Assistant with docker by running:

```sh
npm run start:hass
```

Once it's done, go to Home Assistant instance [http://localhost:8123](http://localhost:8123) and start configuration.

#### Windows Users

If you are on Windows, either run the above command in Powershell, or use the below if using Command Prompt:

```sh
npm run start:hass-cmd
```

### Development

In another terminal, install dependencies and run development server:

```sh
npm install
npm start
```

Server will start on port `4000`.

### Build

You can build the `mushroom.js` file in `dist` folder by running the build command.

```sh
npm run build
```

### Translations

If you want to help translating Mushroom, you can translate it directly from your browser using [Weblate][weblate-url].

### Maintainer steps to add a new language

1. To be compatible with Home Assistant, language tags have to follow [BCP 47](https://www.rfc-editor.org/info/bcp47). A list of most language tags can be found here: [IANA subtag registry](http://www.iana.org/assignments/language-subtag-registry/language-subtag-registry). Examples: `fr`, `fr-CA`, `zh-Hans`.
2. Create a new file `{language_code}.json` with your language code in the [translation folder](https://github.com/piitaya/lovelace-mushroom/tree/main/src/translations). Examples: `fr.json`.
3. Import your file into the [`localize.ts file`](https://github.com/piitaya/lovelace-mushroom/blob/main/src/localize.ts) and add your language in the `languages` record.
4. Don't forget to test locally with the development server by choosing the language with the Home Assistant UI in your profile.

## Troubleshooting

### I don't see the last changes

1. Check that your Home Assistant version is the latest. Some new Mushroom features can only be visible for the latest Home Assistant version.
2. Check that you have the latest Mushroom version on HACS
3. Check that you have the latest Mushroom version by checking the browser console
4. Clear your cache :
   - delete mushroom resources (https://my.home-assistant.io/redirect/lovelace_resources/)
   - uninstall Mushroom from HACS
   - reinstall Mushroom from HACS

### My card mod configuration doesn't work.

Help about card mod configuration is not provided in this repository. More info in the [state of card mod support](https://github.com/piitaya/lovelace-mushroom/issues/1366).

## Credits

The design is inspired by [7ahang’s work][7ahang] on Behance and [Ui Lovelace Minimalist][ui-lovelace-minimalist].

<!-- Badges -->

[hacs-url]: https://github.com/hacs/integration
[hacs-badge]: https://img.shields.io/badge/hacs-default-orange.svg?style=flat-square
[release-badge]: https://img.shields.io/github/v/release/piitaya/lovelace-mushroom?style=flat-square
[downloads-badge]: https://img.shields.io/github/downloads/piitaya/lovelace-mushroom/total?style=flat-square
[build-badge]: https://img.shields.io/github/actions/workflow/status/piitaya/lovelace-mushroom/build.yml?branch=main&style=flat-square
[translations-badge]: https://hosted.weblate.org/widget/mushroom/svg-badge.svg

<!-- References -->

[home-assistant]: https://www.home-assistant.io/
[home-assitant-theme-docs]: https://www.home-assistant.io/integrations/frontend/#defining-themes
[hacs]: https://hacs.xyz
[ui-lovelace-minimalist]: https://ui-lovelace-minimalist.github.io/UI/
[button-card]: https://github.com/custom-cards/button-card
[7ahang]: https://www.behance.net/gallery/88433905/Redesign-Smart-Home
[release-url]: https://github.com/piitaya/lovelace-mushroom/releases
[weblate-url]: https://hosted.weblate.org/engage/mushroom/
