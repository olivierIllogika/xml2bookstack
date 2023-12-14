#!/usr/bin/env python3
#
# Filename: write_markup.py
# Copyright (C) 2018  Henning Gebhard

import re
from os import makedirs
from os.path import join
import pathlib
from string import Template

from xml2mw.transform import to_mw


def write_mediawiki(pages, path, template):
    """Write a markup file for each page recovered from the XML."""
    makedirs(path, exist_ok=True)
    ext = pathlib.Path(template).suffix

    with open(template) as tmpl_file:
        tmpl = tmpl_file.read()

    for page_id, page_data in pages.items():
        body = page_data.get('body', '')
        body_text = "\n".join(to_mw(body))
        filename = re.sub(r'[\\/*?:"<>|]',"",page_data.get('title', '')) + '_' + str(page_id) + ext
        filepath = join(path, filename)
        data = {
            'body': body_text,
            'title': filename,
            'version': page_data.get('version'),
            'current': page_data.get('contentStatus'),
            'created': page_data.get('creationDate'),
            'latest_mod': page_data.get('lastModificationDate'),
            'position': page_data.get('position'),
        }
        filecontent = Template(tmpl).safe_substitute(data)

        with open(filepath, 'w') as outfile:
            outfile.write(filecontent)
