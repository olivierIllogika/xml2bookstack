# xml2bookstack
Parse confluence xml export and create book, chapters and pages using the bookstBookStackack API.

## Acknowledgment
The forked repo [ben-tinc/xml2mw](https://github.com/ben-tinc/xml2mw) was a great start. Thank you for all the work! 

## Requirements
* Python 3.6 (tested with 3.11.6)
* pipenv
* A [BookStack](https://www.bookstackapp.com/) instance
* A BookStack user with the [Access System API](https://demo.bookstackapp.com/api/docs#authentication) permission
* Emoticons svg files (if your Confluence pages use them)

## Usage
 
 * Clone this repo and `cd xml2bookstack`.
 * Use `pipenv install` to install all dependencies (or ensure for yourself that you use `python3` and that `lxml` and `anytree` are installed). If using `pipenv`, type `pipenv shell` afterwards to enter the virtualenv. Prepend the command with `PIPENV_VENV_IN_PROJECT=1` if you want the virtual environment folder to be created locally. If your python version is greater than 3.6, edit Pipfile to have `python_version = "3"`.
 * Place the `entities.xml` file and `attachements` folder from the confluence export inside a `data` subdirectory (or specify location with -d/--data option).
 * Copy `dot.env.sample` to `.env` and configure for your BookStack instance (url, api token and secret)
 * Copy `emoticons` folder to your BookStack instance {web root}/public/emoticons (optional) 
 * Run `python xml2bookstack.py`.

## Supported / TODO
- [X] Image attachements
- [X] Flatten deep page hierarchy
- [X] Emojis
- [ ] Comments
- [ ] Page order
- [ ] Table formatting (header, color, width)
- [ ] Image size

## Known issues
* Chapter/Page order is wrong
* Error 413 'Request entity too large' - see https://www.bookstackapp.com/docs/admin/upload-config/#changing-upload-limits

## Test suite

If you want to run the test suite, just run `python -m unittest discover`. Using `pytest` should work as well, if you prefer that. `pytest` is included in the development dependencies, which you can install with `pipenv install --dev`. **Test suite is from original xml2mw project**
