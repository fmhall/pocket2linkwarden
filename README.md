<p align="center">
<a href="https://pypi.org/project/pocket2linkwarden/"><img src="https://img.shields.io/pypi/v/pocket2linkwarden?color=%2334D058&label=pypi" /></a>
<a href="https://github.com/fmhall/pocket2linkwarden/issues"><img src="https://img.shields.io/github/issues-raw/fmhall/pocket2linkwarden" /></a>
<img alt="GitHub License" src="https://img.shields.io/github/license/fmhall/pocket2linkwarden">
</p>


# Pocket2Linkwarden

Convert your Pocket bookmarks export to a Linkwarden-compatible HTML file.

## Usage

Go to [Pocket](https://getpocket.com/export/) and click "Export HTML File". Pocket will actually send you a `.csv` file, which is not compatible with Linkwarden's built-in importing feature.

Once you use the download link they send to your email, unzip the `pocket` folder. It should look something like:

```
pocket
├── annotations
│   └── part_000000.json
└── part_000000.csv
```

If you have [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed, you can then simply run:

```bash
uvx pocket2linkwarden <filename.csv>
```

Where filename in this case is `part_000000.csv`. You can optionally specify an output file with `-o`. Once your `bookmarks.html` has been generated, navigate to Linkwarden settings and select the "From Bookmarks HTML File" option.

<img width="329" alt="Screenshot 2025-05-06 at 5 18 35 PM" src="https://github.com/user-attachments/assets/36633de3-2199-4c5d-a491-ae86009e6ca3" />
