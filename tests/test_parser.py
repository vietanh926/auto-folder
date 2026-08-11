from auto_folder.parser import parse_tree


def test_parse_standard_tree():
    nodes = parse_tree(
        """order-sync/\n│\n├── app/\n│   ├── __init__.py\n│   ├── config.py # comment\n│   └── api/\n│       └── routes.py\n└── main.py\n"""
    )

    assert [(n.name, n.level, n.is_dir) for n in nodes] == [
        ("order-sync", 0, True),
        ("app", 1, True),
        ("__init__.py", 2, False),
        ("config.py", 2, False),
        ("api", 2, True),
        ("routes.py", 3, False),
        ("main.py", 1, False),
    ]


def test_parse_markdown_artifacts():
    nodes = parse_tree("""app/\n├── **init**.py\n├── api\\_client.py # comment\n└── config.py\n""")

    assert [n.name for n in nodes] == [
        "app",
        "__init__.py",
        "api_client.py",
        "config.py",
    ]


def test_blank_and_decoration_lines_are_ignored():
    nodes = parse_tree("""project/\n│\n│   \n├── app/\n│\n└── main.py\n""")
    assert [n.name for n in nodes] == ["project", "app", "main.py"]
