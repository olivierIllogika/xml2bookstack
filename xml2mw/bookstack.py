#!/usr/bin/env python3
#
# Filename: bookstack.py
# Copyright (C) 2023 Olivier Martin

import bookstack
import os
from dotenv import load_dotenv
from anytree import Node, PreOrderIter, PostOrderIter
import json

class Confluence2bookstack():
	    
    def __init__(self, base_url, token_id, token_secret):
        self.api = bookstack.BookStack(base_url, token_id=token_id, token_secret=token_secret)
        self.api.generate_api_methods()

    def find_tree_depth(self, site_map):
        depth = 0
        for node in PostOrderIter(site_map):
            if node.depth > depth:
                depth = node.depth
        return depth

    def create_book(self, space_data, pages, site_map):
        result = self.api.post_books_create({'name': space_data['name'], 'description': space_data['description'] or ''})
        self._iterate_sitemap(result['id'], pages, site_map)

    def _iterate_sitemap(self, book_id, pages, site_map):

        def build_deep_page_name(node, top_node):
            if node.parent == top_node:
                return None
            ancestry = build_deep_page_name(node.parent, top_node)
            return (ancestry and ancestry + ' - ' or '') + node.name

        def build_deep_page_prio(node, top_node, max_depth):
            if node.parent == top_node:
                return 0
            priority = build_deep_page_prio(node.parent, top_node, max_depth)
            if node.page['position'] is not None:
                position = int(node.page['position'])
                priority = priority + (position * pow(10, max_depth - node.depth) or position)
            return priority

        max_depth = self.find_tree_depth(site_map)

        top_node = None
        top_page = None
        last_chapter_id = None
        temp_chapter_count = 1
        for node in PreOrderIter(site_map):
            parent_name = ''
            if not node.parent:
                top_node = node
                continue

            if node.page and 'space' in node.page:
                space = node.page['space']
            else:
                # Trash pages
                continue

            children_count = node.children and len(node.children) or 0
            priority = build_deep_page_prio(node, top_node, max_depth)

            if node.parent is top_node:
                last_chapter_id = None
                node_str = f"page {node.name} (home, parent book) priority:{priority}"
                top_page = node
                self._create_page(node.page, node.name, priority, book_id, last_chapter_id)
            elif node.parent is top_page and children_count == 0:
                last_chapter_id = None
                node_str = f"page {node.name} (top page, parent book) priority:{priority}"
                self._create_page(node.page, node.name, priority, book_id, last_chapter_id)
            elif node.parent is top_page and children_count > 0:
                result = self._create_chapter(book_id, node.name, priority, node.page.get('description', ''))
                last_chapter_id = result['id']
                node_str = f"new chapter {node.name} {last_chapter_id} (parent book) and page {node.name} (parent new chapter {last_chapter_id}) priority:{priority}"
                self._create_page(node.page, node.page.get('title', ''), priority+1, book_id, last_chapter_id)
            else:
                name = build_deep_page_name(node, top_page)
                parent = (last_chapter_id and last_chapter_id or 'book')
                node_str = f"page {name} (parent {parent}) priority:{priority}"
                self._create_page(node.page, name, priority, book_id, last_chapter_id)

            print(node_str)

    def _create_chapter(self, book_id, name, priority, description=''):
        return self.api.post_chapters_create({'book_id':book_id, 'name':name, 'description':description, 'priority':priority})

    def _create_page(self, page_data, name, priority, book_id=None, chapter_id=None):

        def print_body_size(body):
            size = len(body)
            size_mb = size / 1024
            print(f"Body size was: {size_mb}mb ({size})")

        body = page_data.get('body', '')

        if body == '':
            # don't create empty pages
            return

        data =  {'name':name, 'html':body, 'priority':priority}
        if chapter_id:
            data['chapter_id'] = chapter_id
        elif book_id:
            data['book_id'] = book_id
        result = self.api.post_pages_create(data)
        if '<html>' in result or '413' in result:
            print(result)
            print_body_size(body)
        elif 'error' in result:
            print(json.dumps(result))
            if result["error"]["code"] == 413:
                print_body_size(body)

    def get_shelves(self):
        # test if we can GET from the bookstack instance
        print(self.api.get_shelves_list())

def to_bookstack(pages, spaces, site_map):
    load_dotenv()

    conf2book = Confluence2bookstack(os.getenv("BOOKSTACK_URL"), os.getenv("BOOKSTACK_TOKEN_ID"), os.getenv("BOOKSTACK_TOKEN_SECRET"))
   
    conf2book.get_shelves()

    for space_id, space_data in spaces.items():
        conf2book.create_book(space_data, pages, site_map)

    print("done!")



