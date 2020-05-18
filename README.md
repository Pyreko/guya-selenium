# guya-selenium

Repo for E2E front-end testing of [guya.moe](https://guya.moe).

## To use

Optionally set up a venv. Then, install the requirements:

```bash
pip install -r requirements.txt
```

Next, download the appropriate drivers. Firefox needs [GeckoDriver](https://github.com/mozilla/geckodriver/releases),
Chrome needs [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads), etc. for whatever platforms you are testing.

TODO: Make controlling which drivers run easier

Finally, run via:

```bash
pytest
```

You can also mess around with flags and whatnot.
