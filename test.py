def main():
    c = [1, 2]

    try:
        for _ in range(3):
            c.pop()
    except IndexError:
        print("error")

    print(c)


if __name__ == '__main__':
    main()
