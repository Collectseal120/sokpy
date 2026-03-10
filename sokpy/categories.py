from bs4 import BeautifulSoup
import requests
from .products import SOKProduct
from typing import List


class SOKCategory:
    def __init__(self, store: "SOKStore", slug, parent=None): # type: ignore
        self.store = store
        self.slug = slug
        self.parent = parent
        self.children: dict[str, "SOKCategory"] = {}
        self._loaded = False

    @property
    def path(self):
        if self.parent:
            return f"{self.parent.path}/{self.slug}"
        return self.slug

    def _load_children(self):
        if self._loaded:
            return

        url = f"https://www.s-kaupat.fi/tuotteet/{self.path}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("div", {"class": "item-name"})

        for item in items:
            href = item.parent["href"]
            child_slug = href.split("/")[-1]
            child = SOKCategory(self.store, child_slug, parent=self)
            self.add_child(child)

        self._loaded = True

    def add_child(self, child: "SOKCategory"):
        self.children[child.slug] = child

    def __getattr__(self, name: str) -> "SOKCategory":
        self._load_children()
        for slug, child in self.children.items():
            if slug.replace("-", "_") == name:
                return child
        raise AttributeError(name)

    def products(self, limit: int = 10) -> list["SOKProduct"]:
        return self.store.get_filtered_products(self.path, limit)
    def __str__(self):
            return f"<SOKCategory slug='{self.slug}' path='{self.path}' children={list(self.children.keys())}>"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "slug": self.slug,
            "parent": self.parent,
            "children": self.children,
        }


class SOKCategories:
    def __init__(self, store):
        self.store = store
        self.root: dict[str, SOKCategory] = {}
        self._loaded = False

    def _load_root_categories(self):
        if self._loaded:
            return

        url = "https://www.s-kaupat.fi/tuotteet"
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.find_all("div", {"class": "item-name"})
        for item in items:
            href = item.parent["href"]
            slug = href.split("/")[-1]

            cat = SOKCategory(self.store, slug)
            self.add_root(cat)

        self._loaded = True

    def add_root(self, category: "SOKCategory"):
        self.root[category.slug] = category

    def __getattr__(self, name: str) -> "SOKCategory":
        self._load_root_categories()

        for slug, cat in self.root.items():
            if slug.replace("-", "_") == name:
                return cat

        raise AttributeError(name)
    def __str__(self):
            return f"<SOKCategories roots={list(self.root.keys())}>"

    def __repr__(self):
        return self.__str__()
