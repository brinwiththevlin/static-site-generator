from textnode import TextNode, TextType


print("hello world")


def main():
    node = TextNode("fake text", TextType.BOLD, "example.com")
    print(node.text_type)
    pass


if __name__ == "__main__":
    main()
