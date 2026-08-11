from auto_folder.parser import parse_tree


def names(nodes):
    return [(n.name, n.level, n.is_dir) for n in nodes]


def test_unicode_tree_with_comments():
    assert names(parse_tree("""order-sync/\n│\n├── app/\n│   ├── __init__.py\n│   ├── config.py # environment\n│   └── api/\n│       └── routes.py\n└── main.py\n""")) == [
        ("order-sync", 0, True),
        ("app", 1, True),
        ("__init__.py", 2, False),
        ("config.py", 2, False),
        ("api", 2, True),
        ("routes.py", 3, False),
        ("main.py", 1, False),
    ]


def test_markdown_artifacts():
    nodes = parse_tree("""app/\n├── **init**.py\n├── api\\_client.py # HTTP client\n└── config.py\n""")
    assert [n.name for n in nodes] == ["app", "__init__.py", "api_client.py", "config.py"]


def test_ascii_tree():
    nodes = parse_tree("""project/\n+-- app/\n|   +-- main.py\n|   \\-- config.py\n\\-- README.md\n""")
    assert names(nodes) == [
        ("project", 0, True),
        ("app", 1, True),
        ("main.py", 2, False),
        ("config.py", 2, False),
        ("README.md", 1, False),
    ]


def test_fenced_markdown_block():
    text = """Here is the structure:\n\n```text\nproject/\n├── app/\n│   └── main.py\n└── README.md\n```\n\nThis is the end.\n"""
    assert [n.name for n in parse_tree(text)] == ["project", "app", "main.py", "README.md"]


def test_directories_are_inferred_from_children():
    nodes = parse_tree("""project\n    app\n        main.py\n    tests\n        test_main.py\n    README.md\n""")
    assert [(n.name, n.is_dir) for n in nodes] == [
        ("project", True),
        ("app", True),
        ("main.py", False),
        ("tests", True),
        ("test_main.py", False),
        ("README.md", False),
    ]


def test_special_files_and_hidden_files():
    nodes = parse_tree("""project/\n├── .env\n├── .gitignore\n├── Dockerfile\n├── Makefile\n└── LICENSE\n""")
    assert [n.name for n in nodes] == [
        "project", ".env", ".gitignore", "Dockerfile", "Makefile", "LICENSE"
    ]
    assert all(not n.is_dir for n in nodes[1:])


def test_decoration_only_lines_are_ignored():
    nodes = parse_tree("""project/\n│\n│   \n├── app/\n│\n└── main.py\n""")
    assert [n.name for n in nodes] == ["project", "app", "main.py"]
