i = 1;
while (i <= 10) {
    if (i == 5) {
        i = i + 1;
        continue;
    }
    print(i);
    if (i == 8) {
        break;
    }
    i = i + 1;
}
