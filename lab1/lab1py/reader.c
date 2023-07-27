#include <stdio.h>
#include <string.h>

typedef void (*LineCallback)(const char *);

void read_file_line_by_line(const char *filename, LineCallback callback) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file");
        return;
    }

    char line[256];
    while (fgets(line, sizeof(line), file)) {
        // Remove newline character at the end of the line
        size_t len = strlen(line);
        if (len > 0 && line[len - 1] == '\n') {
            line[len - 1] = '\0';
        }

        if (line[0] == '#') continue;

        char *token = strtok(line, " ");

        while (token != NULL) {
            printf("%s\n", token);
            token = strtok(NULL, " ");
        }

        // Call the callback function with the line
        callback(line);
    }

    fclose(file);
}
