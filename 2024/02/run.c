#include <stdio.h>
#include <stdlib.h>

#define SIZE 1024
#define NUMS 20

int issafe(int* levels, int size) {
    int safe = 1, isAsc, distOk;

    isAsc = levels[0] < levels[1];
    for (int i = 0, unsafes = 0; i < size - 1 && safe; i++) {
        distOk = abs(levels[i] - levels[i+1]) <= 3;
        if (isAsc) {
            safe = levels[i] < levels[i+1] && distOk;
        } else {
            safe = levels[i] > levels[i+1] && distOk;
        }
    }
    return safe;
}

int isdampsafe(int* levels, int size, int ignore) {
    int safe = 1, isAsc, distOk, end, next;

    end = ignore == size-1 ? size - 2 : size - 1;
    if (ignore == 0) {
        isAsc = levels[1] < levels[2];
    } else if (ignore == 1) {
        isAsc = levels[0] < levels[2];
    } else {
        isAsc = levels[0] < levels[1];
    }
    for (int i = 0; i < end && safe; i++) {
        if (i == ignore) continue;

        next = i+1;
        if (next == ignore) next = i+2;

        distOk = abs(levels[i] - levels[next]) <= 3;
        if (isAsc) {
            safe = levels[i] < levels[next] && distOk;
        } else {
            safe = levels[i] > levels[next] && distOk;
        }
    }
    return safe;
}


int main(int argc, char** argv) {
    int success = 1, parsed = 1, sum = 0;
    int number, i, offset, bytes_read, lines = 0;
    FILE *f;
    char buff[SIZE];
    int line[NUMS];
    int safe[SIZE];

    for (int i = 0; i < SIZE; i++) {
        buff[i] = 0;
        line[i] = 0;
        safe[i] = 0;
    }

    f = fopen("in.txt", "r");
    while (success) {
        success = fgets(buff, SIZE, f) == buff;
        if (!success) break;
        /* printf("String read: %s", buff); */
        i = 0;
        offset = 0;
        bytes_read = 0;
        do {
            parsed = sscanf(&(buff[offset]), "%d%n", &number, &bytes_read);
            if (parsed != 1) break;

            offset += bytes_read;
            line[i++] = number;
        } while (parsed == 1);

        for (int j=0; j < i; j++) {
            if (isdampsafe(line, i, j)) {
                safe[lines] = 1;
                break;
            }
        }
        lines++;
    }
    fclose(f);

    for (i = 0; i < lines; i++) {
        sum += safe[i];
    }
    printf("sum=%d\n", sum);
    return 0;
}
