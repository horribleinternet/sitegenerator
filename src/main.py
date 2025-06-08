import textnode

def main():
    node = textnode.TextNode("This is some anchor text", textnode.TextType.LINK, "https://www.boot.dev")
    print(node)

main()
